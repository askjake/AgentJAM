import dynamic from 'next/dynamic';
import { FC, useEffect, useMemo, useRef, useState, useCallback } from 'react';
import { Sender } from '@ant-design/x';
import { Button, Dropdown, Flex, MenuProps, message } from 'antd';
import { VscLightbulbSparkle, VscSettings } from 'react-icons/vsc';
import { CloseOutlined, CloudUploadOutlined } from '@ant-design/icons';

import { useAppSelector } from '@shared/ui/store';
import usePrevious from '@shared/ui/hooks/usePrevious.hook';
import { uploadAttachments } from '@shared/ui/services/attachments.services';
import { dexieDb } from '@shared/ui/libs/dexie.libs';
import { isIndexedDBSupported } from '@shared/ui/utils/common.utils';
import useHandleError from '@shared/ui/hooks/useHandleError.hook';
import { checkAttachmentValidator } from '@shared/ui/validators/attachments.validators';

import { StyledChatSenderWrapper } from '@shared/ui/components/molecules/Chat/ChatSender/ChatSender.styled';
import SenderHeaderBlock from '../SenderHeaderBlock';
const AttachmentButton = dynamic(
  () => import('@shared/ui/components/molecules/Chat/AttachmentButton'),
);

import { AttachmentType, FileType } from '@shared/ui/types/attachments.types';
import { ChatStatusEnum } from '@shared/ui/enums/chats.enums';
import { SenderHeaderBlockRef } from '@shared/ui/components/molecules/Chat/SenderHeaderBlock/SenderHeaderBlock.props';
import { ChatSenderProps } from '@shared/ui/components/molecules/Chat/ChatSender/ChatSender.props';

const items: MenuProps['items'] = [
  {
    key: '0',
    label: 'Tools',
    disabled: true,
  },
  {
    type: 'divider',
  },
  {
    key: '1',
    label: 'Enable Reasoning',
    icon: <VscLightbulbSparkle />,
  },
];

const ChatSender: FC<ChatSenderProps> = ({
  onRequest,
  activeChat = null,
  className = '',
}) => {
  const handleError = useHandleError();
  const [selectedKey, setSelectedKey] = useState<string[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [attachmentsList, setAttachmentsList] = useState<AttachmentType[]>([]);
  const [headerOpen, setHeaderOpen] = useState(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [dragging, setDragging] = useState(false);
  const dragCounterRef = useRef(0);
  const [attachedFiles, setAttachedFiles] = useState<FileType[]>([]);
  const aiTyping = useAppSelector((store) => store.chats.aiTyping);
  const collapsedSidebar = useAppSelector(
    (store) => store.settings.collapsedSidebar,
  );
  const senderHeaderBlockRef = useRef<SenderHeaderBlockRef>(null);
  const prevChatId = usePrevious(activeChat?.chat_id);
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);

  const isReadyOnlyChat = useMemo(
    () => activeChat?.status === ChatStatusEnum.READONLY,
    [activeChat],
  );

  // Load draft message on mount or when chat changes
  useEffect(() => {
    if (isIndexedDBSupported()) {
      const loadDraftMessage = async () => {
        if (activeChat?.chat_id) {
          try {
            const draft = await dexieDb.draftMessages.get(activeChat.chat_id);
            if (draft?.message) {
              setNewMessage(draft.message);
            }
          } catch (e) {
            handleError(e);
          }
        }
      };

      loadDraftMessage();
    }
  }, [activeChat?.chat_id]);

  // Clear draft when switching chats
  useEffect(() => {
    if (prevChatId && activeChat?.chat_id !== prevChatId) {
      setNewMessage('');
      senderHeaderBlockRef?.current?.resetAttachments?.();
      setAttachmentsList([]);
    }
  }, [activeChat, prevChatId]);

  // Debounced save to IndexedDB
  const saveDraftMessage = useCallback(
    (message: string) => {
      if (!activeChat?.chat_id) return;

      // Clear existing timer
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }

      // Set new timer
      debounceTimerRef.current = setTimeout(async () => {
        try {
          if (message.trim()) {
            await dexieDb.draftMessages.put({
              chat_id: activeChat.chat_id,
              message,
              updated_at: new Date(),
            });
          } else {
            // Remove draft if message is empty
            await dexieDb.draftMessages.delete(activeChat.chat_id);
          }
        } catch (e) {
          handleError(e);
        }
      }, 500);
    },
    [activeChat?.chat_id],
  );

  // Cleanup debounce timer on unmount
  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  const handleMessageChange = (value: string) => {
    setNewMessage(value);
    if (isIndexedDBSupported()) {
      saveDraftMessage(value);
    }
  };

  const onSubmit = async (nextContent: string) => {
    if (!nextContent) return;
    try {
      setNewMessage('');
      setHeaderOpen(false);
      senderHeaderBlockRef?.current?.resetAttachments?.();

      await onRequest({
        content: nextContent,
        attachments: attachmentsList,
        selectedKey,
      });
      // Remove draft from IndexedDB after successful send
      if (activeChat?.chat_id && isIndexedDBSupported()) {
        await dexieDb.draftMessages.delete(activeChat.chat_id);
      }
    } catch (e) {
      console.error(e);
      setNewMessage(nextContent);
    } finally {
      setAttachmentsList([]);
    }
  };

  const onAddAttachment = async (
    files: FileType[],
  ): Promise<{ attachments: AttachmentType[] }> => {
    const { attachments = [] } = await uploadAttachments(files);
    setAttachmentsList((prev) => [...prev, ...attachments]);
    return {
      attachments,
    };
  };

  const onRemoveAttachment = (attachment_id: string) => {
    setAttachmentsList((prev) =>
      prev.filter((item) => item.attachment_id !== attachment_id),
    );
  };

  // Drag and drop handlers for always-active drop zone
  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounterRef.current++;
    if (dragCounterRef.current === 1 && !isReadyOnlyChat && !aiTyping) {
      setDragging(true);
    }
  }, [isReadyOnlyChat, aiTyping]);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragCounterRef.current--;
    if (dragCounterRef.current === 0) {
      setDragging(false);
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(false);
    dragCounterRef.current = 0;

    if (isReadyOnlyChat || aiTyping || loading) {
      message.warning('Cannot upload files at this time');
      return;
    }

    const droppedFiles = Array.from(e.dataTransfer.files);
    if (droppedFiles.length === 0) return;

    // Convert to FileType format
    const fileObjects: FileType[] = droppedFiles.map((file, index) => ({
      uid: `drop-${Date.now()}-${index}`,
      name: file.name,
      status: 'uploading',
      originFileObj: file,
    }));

    // Validate files using existing validator
    const validFiles: FileType[] = [];
    for (const fileObj of fileObjects) {
      const { success, error } = checkAttachmentValidator.safeParse({
        attachment: fileObj.originFileObj,
      });

      if (success) {
        // Check for duplicates
        const isDuplicate = attachedFiles.some(f => f.name === fileObj.name);
        if (!isDuplicate) {
          validFiles.push(fileObj);
        } else {
          message.warning(`File "${fileObj.name}" is already attached`);
        }
      } else {
        const formattedError = error?.format();
        const errorMessage = formattedError?.attachment?._errors[0];
        if (errorMessage) {
          message.error(`${fileObj.name}: ${errorMessage}`);
        }
      }
    }

    if (validFiles.length > 0) {
      // Add to attached files state
      setAttachedFiles(prev => [...prev, ...validFiles]);
      
      // Open header to show files
      setHeaderOpen(true);
      
      // Tell the ref to add these files
      senderHeaderBlockRef.current?.addFiles?.(validFiles);
      
      message.success(`Added ${validFiles.length} file(s) for upload`);
    }
  }, [isReadyOnlyChat, aiTyping, loading, attachedFiles, setHeaderOpen]);

    const renderToolButton = (key = '') => {
    if (key === '1') {
      return (
        <Button
          color='primary'
          disabled={loading || aiTyping}
          variant='filled'
          icon={<VscLightbulbSparkle />}
          onClick={() => setSelectedKey([])}
        >
          <span>Reasoning</span>
          <CloseOutlined />
        </Button>
      );
    }
    return;
  };

  return (
    <StyledChatSenderWrapper
      $collapsedSidebar={collapsedSidebar}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      style={{ position: 'relative' }}
    >
      {dragging && !isReadyOnlyChat && !aiTyping && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(24, 144, 255, 0.1)',
            border: '2px dashed #1890ff',
            borderRadius: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              textAlign: 'center',
              color: '#1890ff',
              fontSize: '18px',
              fontWeight: 'bold',
            }}
          >
            <CloudUploadOutlined style={{ fontSize: '48px', display: 'block', margin: '0 auto 16px' }} />
            <div>Drop log files here to upload</div>
            <div style={{ fontSize: '14px', marginTop: '8px', fontWeight: 'normal' }}>
              Supports .log, .log.1, .gz, .zip, .tar and more
            </div>
          </div>
        </div>
      )}
      <Sender
        className={`chat-sender ${className}`}
        value={newMessage}
        suffix={false}
        header={
          <SenderHeaderBlock
            onAddAttachment={onAddAttachment}
            onRemoveAttachment={onRemoveAttachment}
            open={headerOpen}
            onOpenChange={setHeaderOpen}
            setLoading={setLoading}
            componentRef={senderHeaderBlockRef}
          />
        }
        onSubmit={onSubmit}
        onChange={handleMessageChange}
        footer={(_, { components }) => {
          const { SendButton, LoadingButton } = components;
          return (
            <Flex justify='space-between' align='center'>
              <Flex gap='small' align='center'>
                <AttachmentButton
                  setHeaderOpen={setHeaderOpen}
                  headerOpen={headerOpen}
                  hasFiles={!!attachmentsList.length}
                  disabled={loading || isReadyOnlyChat || aiTyping}
                />
                <Dropdown
                  trigger={['click']}
                  menu={{
                    items,
                    disabled: loading || aiTyping,
                    selectable: true,
                    selectedKeys: selectedKey,
                    onClick: ({ key }) =>
                      setSelectedKey((prev) =>
                        prev.includes(key) ? [] : [key],
                      ),
                  }}
                >
                  <Button
                    type='text'
                    shape='circle'
                    icon={<VscSettings />}
                    disabled={loading || isReadyOnlyChat || aiTyping}
                  />
                </Dropdown>
                {renderToolButton(selectedKey[0])}
              </Flex>
              <Flex align='center'>
                {loading || aiTyping ? (
                  <LoadingButton type='default' />
                ) : (
                  <SendButton type='primary' disabled={isReadyOnlyChat} />
                )}
              </Flex>
            </Flex>
          );
        }}
        loading={loading || aiTyping}
        disabled={isReadyOnlyChat}
      />
    </StyledChatSenderWrapper>
  );
};

export default ChatSender;

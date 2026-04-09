import { SenderHeaderProps } from '@ant-design/x/es/sender/SenderHeader';

import {
  AttachmentStatusResponseType,
  AttachmentType,
  FileType,
} from '@shared/ui/types/attachments.types';
import { RefObject } from 'react';

export interface SenderHeaderBlockProps extends SenderHeaderProps {
  onAddAttachment: (
    value: FileType[],
  ) => Promise<{ attachments: AttachmentType[] }>;
  onRemoveAttachment: (value: string) => void;
  setLoading: (loading: boolean) => void;
  componentRef: RefObject<SenderHeaderBlockRef | null>;
  attachedFiles?: FileType[];  // NEW: Allow parent to control files
  setAttachedFiles?: (files: FileType[] | ((prev: FileType[]) => FileType[])) => void;  // NEW: Parent state setter
}

export type SenderHeaderBlockRef = {
  resetAttachments: () => void;
  addFiles: (files: FileType[]) => void;  // NEW: Method to add files from parent
};

import axiosLibs from '@shared/ui/libs/axios.libs';
import { AttachmentType, FileType } from '@shared/ui/types/attachments.types';
import { uploadAttachmentsValidator } from '@shared/ui/validators/attachments.validators';

export const uploadAttachments = async (
  fileList: FileType[],
): Promise<{ attachments: AttachmentType[] }> => {
  const dataTransfer = new DataTransfer();
  fileList.forEach((item) => {
    if (item.originFileObj instanceof File) {
      dataTransfer.items.add(item.originFileObj);
    }
  });
  await uploadAttachmentsValidator.parse({
    attachments: dataTransfer.files,
  });

  const formData = new FormData();
  fileList.forEach((file) => {
    formData.append('attachments', file.originFileObj as File);
  });

  // Use 60 second timeout for file uploads
  const { data } = await axiosLibs.post(`/attachments`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 60000, // 60 seconds for file uploads
  });
  return data;
};

export const getAttachmentStatuses = async (
  attachment_ids: string[],
): Promise<Record<string, { status: string; progress?: number }>> => {
  const { data } = await axiosLibs.post(`/attachments/status`, {
    attachment_ids,
  });
  return data;
};

export const getAttachment = async (id: string): Promise<AttachmentType> => {
  const { data } = await axiosLibs.get(`/attachments/${id}`);
  return data;
};

export const deleteAttachment = async (id: string) => {
  const { data } = await axiosLibs.delete(`/attachments/${id}`);
  return data;
};

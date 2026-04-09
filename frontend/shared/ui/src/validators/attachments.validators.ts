import { z } from 'zod';

import {
  ALLOWED_DOCUMENTS_MIME_TYPES,
  ALLOWED_IMAGES_MIME_TYPES,
  ALLOWED_LOG_MIME_TYPES,
  MAX_DOCUMENT_COUNT,
  MAX_FILE_SIZE,
  MAX_IMAGE_COUNT,
  MAX_LOG_COUNT,
} from '@shared/ui/constants/validation.constants';
import { categorizeFiles } from '@shared/ui/utils/validation.utils';
import { isServer } from '@shared/ui/constants/common.constants';

// Helper to check if file is a log file based on extension
const isLogFile = (filename: string): boolean => {
  const lowerName = filename.toLowerCase();
  return (
    lowerName.endsWith('.log') ||
    /\.log\.\d+$/.test(lowerName) ||  // .log.1, .log.2, etc.
    lowerName.endsWith('.gz') ||
    lowerName.endsWith('.gzip') ||
    lowerName.endsWith('.zip') ||
    lowerName.endsWith('.tar') ||
    lowerName.endsWith('.tar.gz') ||
    lowerName.endsWith('.tgz')
  );
};

export const checkAttachmentValidator = z.object({
  attachment: z
    .instanceof(File)
    .refine(
      (file) => {
        // Build allowed types object
        const allowedTypes: {
          [key: string]: boolean;
        } = {
          ...Object.keys(ALLOWED_IMAGES_MIME_TYPES).reduce(
            (acc, type) => ({ ...acc, [type]: true }),
            {},
          ),
          ...Object.keys(ALLOWED_DOCUMENTS_MIME_TYPES).reduce(
            (acc, type) => ({ ...acc, [type]: true }),
            {},
          ),
          ...Object.keys(ALLOWED_LOG_MIME_TYPES).reduce(
            (acc, type) => ({ ...acc, [type]: true }),
            {},
          ),
        };
        
        // Check MIME type or file extension for log files
        return allowedTypes[file.type] || isLogFile(file.name);
      },
      {
        message:
          'Invalid file type. Allowed types: JPG, JPEG, PNG, GIF, WEBP, TXT, PDF, DOC, DOCX, LOG, ZIP, GZ, TAR',
      },
    )
    .refine((file) => file.size <= MAX_FILE_SIZE, {
      message: `File size should not exceed ${MAX_FILE_SIZE / (1024 * 1024)}MB`,
    }),
});

const validateFiles = (files: File[]) => {
  const { images, documents } = categorizeFiles(files);
  
  // Categorize log files
  const logs = files.filter(f => isLogFile(f.name));
  
  const allowedTypes = {
    ...ALLOWED_IMAGES_MIME_TYPES,
    ...ALLOWED_DOCUMENTS_MIME_TYPES,
    ...ALLOWED_LOG_MIME_TYPES,
  };

  const validations = [
    {
      condition: images.length > MAX_IMAGE_COUNT,
      error: {
        type: 'image_count',
        message: `Maximum ${MAX_IMAGE_COUNT} images allowed`,
        details: {
          current: images.length,
          maximum: MAX_IMAGE_COUNT,
          files: images.map((f) => ({ name: f.name, type: f.type })),
        },
      },
    },
    {
      condition: documents.length > MAX_DOCUMENT_COUNT,
      error: {
        type: 'document_count',
        message: `Maximum ${MAX_DOCUMENT_COUNT} documents allowed`,
        details: {
          current: documents.length,
          maximum: MAX_DOCUMENT_COUNT,
          files: documents.map((f) => ({ name: f.name, type: f.type })),
        },
      },
    },
    {
      condition: logs.length > MAX_LOG_COUNT,
      error: {
        type: 'log_count',
        message: `Maximum ${MAX_LOG_COUNT} log files allowed`,
        details: {
          current: logs.length,
          maximum: MAX_LOG_COUNT,
          files: logs.map((f) => ({ name: f.name, type: f.type })),
        },
      },
    },
    {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-expect-error
      condition: files.some((file) => !allowedTypes[file.type] && !isLogFile(file.name)),
      error: {
        type: 'invalid_type',
        message:
          'Invalid file type. Allowed types: JPG, JPEG, PNG, GIF, WEBP, TXT, PDF, DOC, DOCX, LOG, ZIP, GZ, TAR',
        details: {
          files: files
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-expect-error
            .filter((file) => !allowedTypes[file.type] && !isLogFile(file.name))
            .map((f) => ({ name: f.name, type: f.type })),
        },
      },
    },
    {
      condition: files.some((file) => file.size > MAX_FILE_SIZE),
      error: {
        type: 'invalid_size',
        message: `File size should not exceed ${MAX_FILE_SIZE / (1024 * 1024)}MB`,
        details: {
          files: files
            .filter((file) => file.size > MAX_FILE_SIZE)
            .map((f) => ({ name: f.name, type: f.type, size: f.size })),
        },
      },
    },
  ];

  const failedValidation = validations.find((v) => v.condition);
  return failedValidation
    ? { isValid: false, error: failedValidation.error }
    : { isValid: true };
};

export const uploadAttachmentsValidator = z.object({
  attachments: isServer
    ? z.any()
    : z
        .instanceof(FileList)
        .refine((list) => list.length > 0, 'At least one file is required')
        .transform((list) => Array.from(list))
        .refine(
          (files) => validateFiles(files).isValid,
          // @ts-ignore
          (files) => ({ message: JSON.stringify(validateFiles(files).error) }),
        ),
});

export type UpdateAttachmentsSchema = z.infer<
  typeof uploadAttachmentsValidator
>;

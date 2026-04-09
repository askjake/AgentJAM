export const MAX_FILE_SIZE = 20 * 1024 * 1024;

export const ALLOWED_IMAGES_MIME_TYPES = {
  'image/jpeg': ['.jpg', '.jpeg'],
  'image/png': ['.png'],
  'image/gif': ['.gif'],
  'image/webp': ['.webp'],
} as const;

export const ALLOWED_DOCUMENTS_MIME_TYPES = {
  'text/plain': ['.txt'],
  'application/pdf': ['.pdf'],
  'application/msword': ['.doc'],
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': [
    '.docx',
  ],
} as const;

// Log files and archives - for log assist analysis
export const ALLOWED_LOG_MIME_TYPES = {
  'text/plain': ['.log'],  // Plain log files
  'text/x-log': ['.log'],  // Some systems use this MIME type
  'application/x-log': ['.log'],  // Alternative log MIME type
  'application/zip': ['.zip'],  // Zipped logs
  'application/gzip': ['.gz', '.gzip'],  // Gzipped logs
  'application/x-gzip': ['.gz'],  // Alternative gzip MIME
  'application/x-tar': ['.tar'],  // Tar archives
  'application/x-compressed-tar': ['.tar.gz', '.tgz'],  // Compressed tar
  'application/octet-stream': ['.log', '.log.1', '.log.2', '.log.3', '.log.4', '.log.5', '.log.6', '.log.7', '.log.8', '.log.9', '.gz', '.zip'],  // Generic binary (numbered logs often use this)
} as const;

export const ALLOWED_FILES_MIME_TYPES = [
  ...Object.values(ALLOWED_IMAGES_MIME_TYPES).flat(),
  ...Object.values(ALLOWED_DOCUMENTS_MIME_TYPES).flat(),
  ...Object.values(ALLOWED_LOG_MIME_TYPES).flat(),
] as const;

export const ALLOWED_FILES_MIME_TYPES_STRING =
  ALLOWED_FILES_MIME_TYPES.join(',');

export const MAX_IMAGE_COUNT = 20;

export const MAX_DOCUMENT_COUNT = 20;

export const MAX_LOG_COUNT = 20;

export const ALLOWED_SPECIAL_CHARS = '!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~';

export const MAX_CHATS = 200;

export const MAX_CHATS_GROUPS = 20;

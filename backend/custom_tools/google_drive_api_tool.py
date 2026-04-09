"""
accesses google drive as manager
"""

def google_drive_api_tool(
    action: str,
    file_id: Optional[str] = None,
    file_name: Optional[str] = None,
    file_content: Optional[str] = None,
    mime_type: Optional[str] = None,
    folder_id: Optional[str] = None,
    query: Optional[str] = None,
    permissions: Optional[Dict[str, Any]] = None,
    page_size: int = 100,
    credentials: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Accesses Google Drive as a manager, providing comprehensive file and folder management capabilities.

    This tool enables interactions with Google Drive API to perform various operations
    such as listing, uploading, downloading, updating, deleting files, and managing permissions.

    Args:
        action (str): The operation to perform. Supported actions:
            - 'list_files': List files in Google Drive
            - 'get_file': Retrieve metadata for a specific file
            - 'upload_file': Upload a new file to Google Drive
            - 'update_file': Update an existing file's content or metadata
            - 'delete_file': Delete a file from Google Drive
            - 'create_folder': Create a new folder
            - 'move_file': Move a file to a different folder
            - 'share_file': Share a file with specific permissions
            - 'get_permissions': Get permissions for a file
            - 'search_files': Search for files using a query
            - 'download_file': Download file content
        file_id (Optional[str]): The unique identifier of the file or folder in Google Drive.
            Required for actions: 'get_file', 'update_file', 'delete_file', 'move_file',
            'share_file', 'get_permissions', 'download_file'.
        file_name (Optional[str]): The name of the file or folder.
            Required for actions: 'upload_file', 'create_folder'.
            Optional for 'update_file'.
        file_content (Optional[str]): The content of the file to upload or update.
            Used for actions: 'upload_file', 'update_file'.
        mime_type (Optional[str]): The MIME type of the file (e.g., 'text/plain', 'application/pdf').
            Used for actions: 'upload_file', 'update_file'.
            Defaults to 'text/plain' if not specified for text content.
        folder_id (Optional[str]): The ID of the folder to place the file in.
            Used for actions: 'upload_file', 'create_folder', 'move_file'.
        query (Optional[str]): A search query string following Google Drive query syntax.
            Required for action: 'search_files'.
            Example: "name contains 'report' and mimeType = 'application/pdf'"
        permissions (Optional[Dict[str, Any]]): Permission settings for sharing a file.
            Required for action: 'share_file'.
            Expected keys:
                - 'role' (str): Permission role ('reader', 'writer', 'commenter', 'owner')
                - 'type' (str): Permission type ('user', 'group', 'domain', 'anyone')
                - 'email' (str): Email address (required for 'user' and 'group' types)
                - 'domain' (str): Domain name (required for 'domain' type)
        page_size (int): Maximum number of files to return for list/search operations.
            Defaults to 100. Maximum allowed is 1000.
        credentials (Optional[Dict[str, Any]]): Authentication credentials for Google Drive API.
            Expected keys:
                - 'access_token' (str): OAuth 2.0 access token
                - 'refresh_token' (str): OAuth 2.0 refresh token (optional)
                - 'client_id' (str): OAuth 2.0 client ID (optional)
                - 'client_secret' (str): OAuth 2.0 client secret (optional)
                - 'service_account_key' (dict): Service account key JSON (alternative auth)

    Returns:
        Dict[str, Any]: A dictionary containing the result of the operation with the following keys:
            - 'status' (str): 'success' if the operation completed successfully, 'error' otherwise.
            - 'data' (Any): The result data from the operation. Structure varies by action:
                - 'list_files'/'search_files': List of file metadata dictionaries
                - 'get_file': File metadata dictionary
                - 'upload_file': Uploaded file metadata dictionary
                - 'update_file': Updated file metadata dictionary
                - 'delete_file': Boolean indicating deletion success
                - 'create_folder': Created folder metadata dictionary
                - 'move_file': Updated file metadata dictionary
                - 'share_file': Permission resource dictionary
                - 'get_permissions': List of permission dictionaries
                - 'download_file': File content as string or bytes
                Returns None if an error occurred.
            - 'message' (str): A descriptive message about the operation result or error details.

    Raises:
        No exceptions are raised directly; all errors are caught and returned in the result dict.

    Example:
        >>> result = google_drive_api_tool(
        ...     action='list_files',
        ...     page_size=10,
        ...     credentials={'access_token': 'your_access_token'}
        ... )
        >>> if result['status'] == 'success':
        ...     for file in result['data']:
        ...         print(file['name'])

        >>> result = google_drive_api_tool(
        ...     action='upload_file',
        ...     file_name='report.txt',
        ...     file_content='This is the report content',
        ...     mime_type='text/plain',
        ...     folder_id='folder_id_here',
        ...     credentials={'access_token': 'your_access_token'}
        ... )
        >>> print(result['message'])

        >>> result = google_drive_api_tool(
        ...     action='share_file',
        ...     file_id='file_id_here',
        ...     permissions={
        ...         'role': 'reader',
        ...         'type': 'user',
        ...         'email': 'colleague@example.com'
        ...     },
        ...     credentials={'access_token': 'your_access_token'}
        ... )
    """
    try:
        import json
        import urllib.request
        import urllib.parse
        import urllib.error

        DRIVE_API_BASE_URL = "https://www.googleapis.com/drive/v3"
        DRIVE_UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3"

        def _validate_credentials(creds: Optional[Dict[str, Any]]) -> Optional[str]:
            """Validate and extract access token from credentials."""
            if not creds:
                return None
            if isinstance(creds, dict):
                return creds.get('access_token')
            return None

        def _make_request(
            url: str,
            method: str = "GET",
            headers: Optional[Dict[str, str]] = None,
            body: Optional[bytes] = None
        ) -> Dict[str, Any]:
            """Make an HTTP request to the Google Drive API."""
            if headers is None:
                headers = {}

            request = urllib.request.Request(
                url,
                data=body,
                headers=headers,
                method=method
            )

            with urllib.request.urlopen(request, timeout=30) as response:
                response_body = response.read()
                if response_body:
                    return json.loads(response_body.decode('utf-8'))
                return {}

        def _build_headers(access_token: str, content_type: Optional[str] = None) -> Dict[str, str]:
            """Build HTTP headers with authorization."""
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
            if content_type:
                headers["Content-Type"] = content_type
            return headers

        def _validate_action(act: str) -> bool:
            """Validate if the action is supported."""
            supported_actions = [
                'list_files', 'get_file', 'upload_file', 'update_file',
                'delete_file', 'create_folder', 'move_file', 'share_file',
                'get_permissions', 'search_files', 'download_file'
            ]
            return act in supported_actions

        def _sanitize_query(q: str) -> str:
            """Basic sanitization of query string."""
            dangerous_chars = [';', '--', '/*', '*/']
            sanitized = q
            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')
            return sanitized

        if not action:
            return {
                'status': 'error',
                'data': None,
                'message': "Action parameter is required."
            }

        if not _validate_action(action):
            return {
                'status': 'error',
                'data': None,
                'message': f"Unsupported action: '{action}'. Please use a valid action."
            }

        access_token = _validate_credentials(credentials)
        if not access_token:
            return {
                'status': 'error',
                'data': None,
                'message': "Valid credentials with 'access_token' are required."
            }

        page_size = min(max(1, page_size), 1000)

        if action == 'list_files':
            params = {
                'pageSize': str(page_size),
                'fields': 'files(id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink)',
                'trashed': 'false'
            }
            if folder_id:
                params['q'] = f"'{folder_id}' in parents and trashed=false"

            url = f"{DRIVE_API_BASE_URL}/files?{urllib.parse.urlencode(params)}"
            headers = _build_headers(access_token)
            response_data = _make_request(url, headers=headers)
            files = response_data.get('files', [])

            return {
                'status': 'success',
                'data': files,
                'message': f"Successfully retrieved {len(files)} files."
            }

        elif action == 'get_file':
            if not file_id:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_id is required for 'get_file' action."
                }

            params = {
                'fields': 'id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink,description'
            }
            url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}?{urllib.parse.urlencode(params)}"
            headers = _build_headers(access_token)
            file_data = _make_request(url, headers=headers)

            return {
                'status': 'success',
                'data': file_data,
                'message': f"Successfully retrieved file metadata for '{file_data.get('name', file_id)}'."
            }

        elif action == 'upload_file':
            if not file_name:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_name is required for 'upload_file' action."
                }

            effective_mime_type = mime_type or 'text/plain'
            content_bytes = (file_content or '').encode('utf-8')

            metadata = {
                'name': file_name,
                'mimeType': effective_mime_type
            }
            if folder_id:
                metadata['parents'] = [folder_id]

            boundary = 'boundary_string_12345'
            metadata_json = json.dumps(metadata).encode('utf-8')

            multipart_body = (
                f'--{boundary}\r\n'
                f'Content-Type: application/json; charset=UTF-8\r\n\r\n'
            ).encode('utf-8') + metadata_json + (
                f'\r\n--{boundary}\r\n'
                f'Content-Type: {effective_mime_type}\r\n\r\n'
            ).encode('utf-8') + content_bytes + f'\r\n--{boundary}--'.encode('utf-8')

            url = f"{DRIVE_UPLOAD_URL}/files?uploadType=multipart&fields=id,name,mimeType,size,createdTime,webViewLink"
            headers = _build_headers(
                access_token,
                content_type=f'multipart/related; boundary={boundary}'
            )

            uploaded_file = _make_request(url, method="POST", headers=headers, body=multipart_body)

            return {
                'status': 'success',
                'data': uploaded_file,
                'message': f"Successfully uploaded file '{file_name}' with ID '{uploaded_file.get('id')}'."
            }

        elif action == 'update_file':
            if not file_id:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_id is required for 'update_file' action."
                }

            if file_content is not None:
                effective_mime_type = mime_type or 'text/plain'
                content_bytes = file_content.encode('utf-8')

                metadata = {}
                if file_name:
                    metadata['name'] = file_name

                if metadata:
                    boundary = 'boundary_string_12345'
                    metadata_json = json.dumps(metadata).encode('utf-8')

                    multipart_body = (
                        f'--{boundary}\r\n'
                        f'Content-Type: application/json; charset=UTF-8\r\n\r\n'
                    ).encode('utf-8') + metadata_json + (
                        f'\r\n--{boundary}\r\n'
                        f'Content-Type: {effective_mime_type}\r\n\r\n'
                    ).encode('utf-8') + content_bytes + f'\r\n--{boundary}--'.encode('utf-8')

                    url = f"{DRIVE_UPLOAD_URL}/files/{urllib.parse.quote(file_id)}?uploadType=multipart&fields=id,name,mimeType,modifiedTime"
                    headers = _build_headers(
                        access_token,
                        content_type=f'multipart/related; boundary={boundary}'
                    )
                    updated_file = _make_request(url, method="PATCH", headers=headers, body=multipart_body)
                else:
                    url = f"{DRIVE_UPLOAD_URL}/files/{urllib.parse.quote(file_id)}?uploadType=media&fields=id,name,mimeType,modifiedTime"
                    headers = _build_headers(access_token, content_type=effective_mime_type)
                    updated_file = _make_request(url, method="PATCH", headers=headers, body=content_bytes)
            else:
                metadata = {}
                if file_name:
                    metadata['name'] = file_name
                if mime_type:
                    metadata['mimeType'] = mime_type

                if not metadata:
                    return {
                        'status': 'error',
                        'data': None,
                        'message': "At least one of file_name, file_content, or mime_type must be provided for 'update_file'."
                    }

                url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}?fields=id,name,mimeType,modifiedTime"
                headers = _build_headers(access_token, content_type='application/json')
                body = json.dumps(metadata).encode('utf-8')
                updated_file = _make_request(url, method="PATCH", headers=headers, body=body)

            return {
                'status': 'success',
                'data': updated_file,
                'message': f"Successfully updated file with ID '{file_id}'."
            }

        elif action == 'delete_file':
            if not file_id:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_id is required for 'delete_file' action."
                }

            url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}"
            headers = _build_headers(access_token)

            try:
                request = urllib.request.Request(url, headers=headers, method="DELETE")
                with urllib.request.urlopen(request, timeout=30):
                    pass
                deletion_success = True
            except urllib.error.HTTPError as delete_err:
                if delete_err.code == 204:
                    deletion_success = True
                else:
                    raise

            return {
                'status': 'success',
                'data': True,
                'message': f"Successfully deleted file with ID '{file_id}'."
            }

        elif action == 'create_folder':
            if not file_name:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_name is required for 'create_folder' action."
                }

            metadata = {
                'name': file_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if folder_id:
                metadata['parents'] = [folder_id]

            url = f"{DRIVE_API_BASE_URL}/files?fields=id,name,mimeType,createdTime,webViewLink"
            headers = _build_headers(access_token, content_type='application/json')
            body = json.dumps(metadata).encode('utf-8')
            created_folder = _make_request(url, method="POST", headers=headers, body=body)

            return {
                'status': 'success',
                'data': created_folder,
                'message': f"Successfully created folder '{file_name}' with ID '{created_folder.get('id')}'."
            }

        elif action == 'move_file':
            if not file_id:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_id is required for 'move_file' action."
                }
            if not folder_id:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "folder_id (destination) is required for 'move_file' action."
                }

            get_params = {'fields': 'parents'}
            get_url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}?{urllib.parse.urlencode(get_params)}"
            get_headers = _build_headers(access_token)
            current_file = _make_request(get_url, headers=get_headers)
            current_parents = ','.join(current_file.get('parents', []))

            params = {
                'addParents': folder_id,
                'removeParents': current_parents,
                'fields': 'id,name,parents,modifiedTime'
            }
            url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}?{urllib.parse.urlencode(params)}"
            headers = _build_headers(access_token, content_type='application/json')
            moved_file = _make_request(url, method="PATCH", headers=headers, body=b'{}')

            return {
                'status': 'success',
                'data': moved_file,
                'message': f"Successfully moved file '{file_id}' to folder '{folder_id}'."
            }

        elif action == 'share_file':
            if not file_id:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_id is required for 'share_file' action."
                }
            if not permissions:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "permissions dict is required for 'share_file' action."
                }

            valid_roles = ['reader', 'writer', 'commenter', 'owner', 'organizer', 'fileOrganizer']
            valid_types = ['user', 'group', 'domain', 'anyone']

            perm_role = permissions.get('role')
            perm_type = permissions.get('type')

            if perm_role not in valid_roles:
                return {
                    'status': 'error',
                    'data': None,
                    'message': f"Invalid permission role '{perm_role}'. Must be one of: {valid_roles}"
                }

            if perm_type not in valid_types:
                return {
                    'status': 'error',
                    'data': None,
                    'message': f"Invalid permission type '{perm_type}'. Must be one of: {valid_types}"
                }

            permission_body = {
                'role': perm_role,
                'type': perm_type
            }

            if perm_type in ['user', 'group']:
                email = permissions.get('email')
                if not email:
                    return {
                        'status': 'error',
                        'data': None,
                        'message': f"'email' is required in permissions for type '{perm_type}'."
                    }
                permission_body['emailAddress'] = email
            elif perm_type == 'domain':
                domain = permissions.get('domain')
                if not domain:
                    return {
                        'status': 'error',
                        'data': None,
                        'message': "domain is required in permissions for type 'domain'."
                    }
                permission_body['domain'] = domain

            url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}/permissions?fields=id,role,type,emailAddress"
            headers = _build_headers(access_token, content_type='application/json')
            body = json.dumps(permission_body).encode('utf-8')
            permission_result = _make_request(url, method="POST", headers=headers, body=body)

            return {
                'status': 'success',
                'data': permission_result,
                'message': f"Successfully shared file '{file_id}' with role '{perm_role}' for type '{perm_type}'."
            }

        elif action == 'get_permissions':
            if not file_id:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_id is required for 'get_permissions' action."
                }

            params = {
                'fields': 'permissions(id,role,type,emailAddress,domain,displayName)'
            }
            url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}/permissions?{urllib.parse.urlencode(params)}"
            headers = _build_headers(access_token)
            response_data = _make_request(url, headers=headers)
            perms = response_data.get('permissions', [])

            return {
                'status': 'success',
                'data': perms,
                'message': f"Successfully retrieved {len(perms)} permissions for file '{file_id}'."
            }

        elif action == 'search_files':
            if not query:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "query is required for 'search_files' action."
                }

            sanitized_query = _sanitize_query(query)
            params = {
                'q': sanitized_query,
                'pageSize': str(page_size),
                'fields': 'files(id,name,mimeType,size,createdTime,modifiedTime,parents,webViewLink)'
            }
            url = f"{DRIVE_API_BASE_URL}/files?{urllib.parse.urlencode(params)}"
            headers = _build_headers(access_token)
            response_data = _make_request(url, headers=headers)
            files = response_data.get('files', [])

            return {
                'status': 'success',
                'data': files,
                'message': f"Search returned {len(files)} results for query: '{sanitized_query}'."
            }

        elif action == 'download_file':
            if not file_id:
                return {
                    'status': 'error',
                    'data': None,
                    'message': "file_id is required for 'download_file' action."
                }

            meta_params = {'fields': 'id,name,mimeType'}
            meta_url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}?{urllib.parse.urlencode(meta_params)}"
            headers = _build_headers(access_token)
            file_meta = _make_request(meta_url, headers=headers)
            file_mime = file_meta.get('mimeType', '')

            google_workspace_export_map = {
                'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.google-apps.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/vnd.google-apps.drawing': 'image/png',
                'application/vnd.google-apps.script': 'application/vnd.google-apps.script+json'
            }

            if file_mime in google_workspace_export_map:
                export_mime = google_workspace_export_map[file_mime]
                download_url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}/export?mimeType={urllib.parse.quote(export_mime)}"
            else:
                download_url = f"{DRIVE_API_BASE_URL}/files/{urllib.parse.quote(file_id)}?alt=media"

            request = urllib.request.Request(download_url, headers=headers, method="GET")
            with urllib.request.urlopen(request, timeout=60) as response:
                content = response.read()

            try:
                decoded_content = content.decode('utf-8')
            except UnicodeDecodeError:
                decoded_content = content.hex()

            return {
                'status': 'success',
                'data': decoded_content,
                'message': f"Successfully downloaded file '{file_meta.get('name', file_id)}'."
            }

        return {
            'status': 'error',
            'data': None,
            'message': f"Action '{action}' could not be processed."
        }

    except urllib.error.HTTPError as http_err:
        error_body = ""
        try:
            error_body = http_err.read().decode('utf-8')
        except Exception:
            pass
        return {
            'status': 'error',
            'data': None,
            'message': f"HTTP error {http_err.code}: {http_err.reason}. Details: {error_body}"
        }
    except urllib.error.URLError as url_err:
        return {
            'status': 'error',
            'data': None,
            'message': f"URL error occurred: {str(url_err.reason)}"
        }
    except TimeoutError:
        return {
            'status': 'error',
            'data': None,
            'message': "Request timed out while connecting to Google Drive API."
        }
    except ValueError as val_err:
        return {
            'status': 'error',
            'data': None,
            'message': f"Value error: {str(val_err)}"
        }
    except KeyError as key_err:
        return {
            'status': 'error',
            'data': None,
            'message': f"Missing required key: {str(key_err)}"
        }
    except Exception as e:
        return {
            'status': 'error',
            'data': None,
            'message': f"An unexpected error occurred: {str(e)}"
        }
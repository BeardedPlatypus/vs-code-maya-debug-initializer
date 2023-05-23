#include <windows.h>
#include <stdio.h>
#include <conio.h>
#include <tchar.h>


/// @brief Convert the specified char string to a TCHAR string.
/// @param s The string to convert.
/// @return The converted string.
TCHAR* ConvertString(char* s) {
    TCHAR *result;
    int length;
    #ifdef UNICODE
    length = MultiByteToWideChar(CP_UTF8, 0, s, strlen(s), NULL, 0);
    result = (TCHAR*) malloc(length* sizeof(TCHAR));
    MultiByteToWideChar(CP_UTF8, 0, s, strlen(s), result, length);
    #else
    result = strdup(s);
    length = strlen(result);
    #endif
    return result;
}

/// @brief Create a buffer file with the specified name and size.
/// @param bufferName The name of the buffer.
/// @param bufferSize The size of the buffer.
/// @return The handle to the created buffer file.
HANDLE CreateBufferFile(char* bufferName, DWORD bufferSize) {
    HANDLE hMapFile;

    TCHAR* tBufferName = ConvertString(bufferName);

    hMapFile = CreateFileMapping(
        INVALID_HANDLE_VALUE,
        NULL,
        PAGE_READWRITE,
        0,
        bufferSize,
        tBufferName);

    free(tBufferName);
    return hMapFile;
}

/// @brief Create a buffer from the given file handle and buffer size.
/// @param hMapFile The handle of the buffer file.
/// @param bufferSize The size of the buffer.
/// @return The pointer to the created buffer.
LPVOID CreateBuffer(HANDLE hMapFile, DWORD bufferSize) {
    LPVOID p = MapViewOfFileEx(hMapFile, FILE_MAP_ALL_ACCESS, 0, 0, bufferSize, NULL);
    return p;
}

/// @brief Free the specified buffer.
/// @param pBuffer The buffer to free.
void FreeBuffer(LPVOID pBuffer) {
    UnmapViewOfFile(pBuffer);
}

/// @brief Free the specified buffer file.
/// @param hMapFile The buffer file to free.
void FreeBufferFile(HANDLE hMapFile) {
    CloseHandle(hMapFile);
}


#ifdef AS_EXECUTABLE
/// @brief Read the value written at the specified buffer.
/// @param argc The number of arguments.
/// @param argv The name and size of the buffer.
/// @return The value written at the specified buffer.
int main(int argc, char *argv[]) {
    if (argc < 1) {
        return 1;
    }

    DWORD bufferSize = 2;

    HANDLE hMapFile = CreateBufferFile(argv[1], bufferSize);
    LPVOID pBuffer = CreateBuffer(hMapFile, bufferSize);

    UINT16 res;
    memcpy(&res, pBuffer, bufferSize);
    
    printf("%d", res);
    
    FreeBuffer(pBuffer);
    FreeBufferFile(hMapFile);

    return 0;
}
#endif
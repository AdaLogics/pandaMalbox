#include <iostream>
#include <Windows.h>
#include <TlHelp32.h>
#include <tchar.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

#pragma comment(lib, "User32.lib")

int DisplayResourceNAMessageBox()
{
	TCHAR szExeFileName[0x100];
	GetModuleFileName(NULL, szExeFileName, 0x100);

	int msgboxID = MessageBox(
		NULL,

		(LPCWSTR)szExeFileName,
		(LPCWSTR)L"Currently executing inside",
		MB_OK
	);

	return msgboxID;
}

int main()
{
    std::cout << "Hello World!\n";
	DisplayResourceNAMessageBox();
}
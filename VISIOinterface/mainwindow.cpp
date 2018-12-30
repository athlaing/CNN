#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "ftd2xx.h"
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    FT_STATUS ftStatus;
    FT_DEVICE_LIST_INFO_NODE *devInfo;
    DWORD numDevs;
    // create the device information list

    ftStatus = FT_CreateDeviceInfoList(&numDevs);
    if (ftStatus == FT_OK)
        qDebug() << "Number of devices is" << numDevs;

    /* write */
    FT_HANDLE ftHandle;
    DWORD BytesWritten;
    char TxBuffer[256]; // Contains data to write to device
    TxBuffer[255] = 'c';
    //memset(TxBuffer, 'c', 256); // breaks the fpga
    ftStatus = FT_Open(0, &ftHandle);
    ftStatus |= FT_Purge(ftHandle, FT_PURGE_RX | FT_PURGE_TX);
    if(ftStatus != FT_OK) {
        qDebug() << "// FT_Open failed";
        return;
    }
    ftStatus = FT_Write(ftHandle, TxBuffer, sizeof(TxBuffer), &BytesWritten);
    if (ftStatus == FT_OK) {
        qDebug() << "FT_Write ok";
        qDebug() << BytesWritten;
        qDebug() << TxBuffer[255];
        qDebug() << sizeof(TxBuffer);
        qDebug() << "//////////////////////////";
    }
    else {
        // FT_Write Failed
    }
    /* write end */

    DWORD RxBytes = 10;
    DWORD BytesReceived;
    char RxBuffer[256];

    FT_SetTimeouts(ftHandle,5000,0);
    ftStatus = FT_Read(ftHandle,RxBuffer,RxBytes,&BytesReceived);
    if (ftStatus == FT_OK) {
        if (BytesReceived == RxBytes) {
            qDebug() << "FT_Read ok";
            qDebug() << (int) RxBuffer[0];
            qDebug() << BytesReceived;
            qDebug() << sizeof(RxBuffer);
            qDebug() << "//////////////////////////";
        }
        else {
            // FT_Read Timeout
        }
    }
    else {
    // FT_Read Failed
    }


    FT_Close(ftHandle);
}

MainWindow::~MainWindow()
{
    delete ui;
}
/*
 *
    DWORD EventDWord;
    DWORD TxBytes;
    DWORD RxBytes;
    DWORD BytesWritten;
    char TxBuffer[1];
    TxBuffer[0] = 'a';
    FT_HANDLE ftHandle;
    ftStatus = FT_Open(0, &ftHandle);

    qDebug() << ftStatus;
    ftStatus |= FT_SetUSBParameters(ftHandle, 4096, 4096); // Set USB transfer sizes
    ftStatus |= FT_SetChars(ftHandle, false, 0, false, 0); // Disable event characters
    ftStatus |= FT_SetTimeouts(ftHandle, 5000, 5000); // Set read/write timeouts to 5 sec
    ftStatus |= FT_SetLatencyTimer(ftHandle, 16); // Latency timer at default 16ms
    ftStatus |= FT_SetFlowControl(ftHandle, FT_FLOW_NONE, 0x11, 0x13); // No flow control
    ftStatus |= FT_SetBaudRate(ftHandle, 9600); // Baud rate = 9600
    ftStatus |= FT_SetDataCharacteristics(ftHandle, FT_BITS_8, FT_STOP_BITS_1, FT_PARITY_NONE);
    if (ftStatus != FT_OK)
        qDebug() << "ftStatus not ok " <<  ftStatus; //check for error
    // write
    FT_GetStatus(ftHandle,&RxBytes,&TxBytes,&EventDWord);
    ftStatus = FT_Purge(ftHandle, FT_PURGE_RX | FT_PURGE_TX);
    ftStatus = FT_Write(ftHandle, TxBuffer, sizeof(TxBuffer), &BytesWritten);
    if (ftStatus == FT_OK) {
        qDebug() << "FT_Write ok";
        qDebug() << BytesWritten;
        qDebug() << TxBuffer[0];
        qDebug() << sizeof(TxBuffer);
    }
    else {
        qDebug() << "FT_Write Failed";
    }


    ftStatus = FT_Close(ftHandle);
    if (ftStatus == FT_OK) {
        qDebug() << "closed";
    }
    else {
        qDebug() << "close Failed";
    }
 */

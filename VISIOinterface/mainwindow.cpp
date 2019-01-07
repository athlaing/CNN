#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "QMessageBox"
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow) {
    ui->setupUi(this);
    InitializeWin();
} // MainWindow()

MainWindow::~MainWindow() {
    delete ui;
} // ~MainWindow()

/******************************************************************************
 * void InitializeWin()
 * Include all functionality to initialize the Mainwindow displays
 * ***************************************************************************/
void  MainWindow::InitializeWin() {
    // change window title
    this->setWindowTitle(QString("VISIOinterface"));

} // InitializeWin

/******************************************************************************
 * void InitializeFTDI()
 * Use to initialize ftdi commnucation protocol
 * ***************************************************************************/
void MainWindow::InitializeFTDI() {
    FT_STATUS ftStatus;
    QMessageBox box;

    // Inializes FTDI protocol and flushes data lines
    ftStatus = FT_Open(0, &ftHandle);
    ftStatus |= FT_Purge(ftHandle, FT_PURGE_RX | FT_PURGE_TX);
    if(ftStatus != FT_OK) {
        box.setText("FT_Open failed");
        box.exec();
    } // Open message box error
} // IniailizeFTDI

/******************************************************************************
 * void CloseFTDI()
 * Use to close ftdi commnucation protocol
 * ***************************************************************************/
void MainWindow::CloseFTDI() {
    FT_STATUS ftStatus;
    QMessageBox box;

    //  flushes data lines and close FTDI protocol
    ftStatus = FT_Purge(ftHandle, FT_PURGE_RX | FT_PURGE_TX);
    ftStatus |= FT_Close(ftHandle);
    if(ftStatus != FT_OK) {
        box.setText("FT_CLOSE failed");
        box.exec();
    } // Open message box error
} // IniailizeFTDI

/******************************************************************************
 * void ReadFromFPGA(
 * Use to Read from FPGA
 * ***************************************************************************/
void MainWindow::ReadFromFPGA() {
    FT_STATUS ftStatus;
    QMessageBox box;
    DWORD RxBytes = 10;
    DWORD BytesReceived;

    /* read using FDTI protocol and set timeout */
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
            box.setText("FT_Read Timeout");
            box.exec();
        } // communication failed due to timeout
    } // read worked
    else {
        box.setText("FT_Read failed");
        box.exec();
    } // read failed
} // ReadFromFPGA

/******************************************************************************
 * void SendToFPGA()
 * Use to Write to FPGA
 * ***************************************************************************/
void MainWindow::SendToFPGA() {
    FT_STATUS ftStatus;
    QMessageBox box;
    DWORD BytesWritten;

    TxBuffer[255] = 'c';
    /* write  to FDTI */
    ftStatus = FT_Write(ftHandle, TxBuffer, sizeof(TxBuffer), &BytesWritten);
    if(ftStatus != FT_OK) {
        box.setText("FT_Write failed");
        box.exec();
    } // protocol failed to write
    else {
        qDebug() << "FT_Write ok";
        qDebug() << BytesWritten;
        qDebug() << TxBuffer[255];
        qDebug() << sizeof(TxBuffer);
        qDebug() << "//////////////////////////";
    } // write complete
} // SendToFPGA



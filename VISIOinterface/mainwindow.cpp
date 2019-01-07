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
    CloseFTDI();
    delete ui;
} // ~MainWindow()

/******************************************************************************
 * void InitializeWin()
 * Include all functionality to initialize the Mainwindow displays
 * ***************************************************************************/
void  MainWindow::InitializeWin() {
    // change window title
    this->setWindowTitle(QString("VISIOinterface"));
    // create new menu and action items
    QMenu* portMenu = ui->menuBar->addMenu(tr("Port Setup"));
    QAction* setupFTDI = new QAction(tr("Setup Port"), this);
    QAction* closeFTDI = new QAction(tr("Close Port"), this);
    // insert action items to menu
    portMenu->addAction(setupFTDI);
    portMenu->addAction(closeFTDI);
    // connect action items to functions
    connect(setupFTDI, SIGNAL(triggered()),
            this, SLOT(InitializeFTDI()));
    connect(closeFTDI, SIGNAL(triggered()),
            this, SLOT(CloseFTDI()));
    // sets action for toggling binary,dec, hex
    connect(ui->Binary_B, SIGNAL(toggled(bool)),
            this, SLOT(DisplayTypeChanged(bool)));
    connect(ui->Dec_B, SIGNAL(toggled(bool)),
            this, SLOT(DisplayTypeChanged(bool)));
    connect(ui->Hex_B, SIGNAL(toggled(bool)),
            this, SLOT(DisplayTypeChanged(bool)));
    connect(ui->BinaryR_B, SIGNAL(toggled(bool)),
            this, SLOT(DisplayTypeChanged(bool)));
    connect(ui->DecR_B, SIGNAL(toggled(bool)),
            this, SLOT(DisplayTypeChanged(bool)));
    connect(ui->HexR_B, SIGNAL(toggled(bool)),
            this, SLOT(DisplayTypeChanged(bool)));
    ui->Binary_B->setChecked(true);
    ui->BinaryR_B->setChecked(true);
    // connects for settings values and setting
    memset(TxBuffer, '\0', 256);
    memset(RxBuffer, '\0', 256);
    connect(ui->Value, SIGNAL(valueChanged(int)),
            this, SLOT(SendValueUpdated(int)));
    connect(ui->Index, SIGNAL(valueChanged(int)),
            this, SLOT(SendIndexUpdated(int)));
    // connects for sending and writing
    connect(ui->SendByte, SIGNAL(clicked()),
            this, SLOT(SendToFPGA()));
    connect(ui->SendByteStream, SIGNAL(clicked()),
            this, SLOT(SendToFPGA()));
    // connects for Reading
    connect(ui->ReadFromFPGA_B, SIGNAL(clicked()),
            this, SLOT(ReadFromFPGA()));
    connect(ui->IndexR, SIGNAL(valueChanged(int)),
            this, SLOT(ReadIndexUpdated(int)));
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

/******************************************************************************
 * void DisplayTypeChanged()
 * Changes the display type of the value button in the fpga w/r category
 * ***************************************************************************/
void MainWindow::DisplayTypeChanged(bool) {
    if(ui->Binary_B->isChecked() == true) {
        ui->Value->setDisplayIntegerBase(2);
    } // set display to binary
    else if(ui->Hex_B->isChecked() == true) {
        ui->Value->setDisplayIntegerBase(16);
    } // set display to hex
    else if(ui->Dec_B->isChecked() == true) {
        ui->Value->setDisplayIntegerBase(10);
    } // set display to dec
    if(ui->BinaryR_B->isChecked() == true) {
        ui->ValueR->setDisplayIntegerBase(2);
    } // set display to binary
    else if(ui->HexR_B->isChecked() == true) {
        ui->ValueR->setDisplayIntegerBase(16);
    } // set display to hex
    else if(ui->DecR_B->isChecked() == true) {
        ui->ValueR->setDisplayIntegerBase(10);
    } // set display to dec
} //DisplayTypeChanged()

/******************************************************************************
 * void SendValueUpdated()
 * Updates the TxBuffer based on the displayed values
 * ***************************************************************************/
void MainWindow::SendValueUpdated(int value) {
    int index = ui->Index->value();
    TxBuffer[index] = (char) value;
    QString displayStr;
    QString data;
    for(int i = 255; i >= 0; i--) {
        data = QString("%1").arg((unsigned int) TxBuffer[i], 0, 16);
        displayStr.append(data);
    } // insert all items
    ui->ValuePreview->setText(displayStr);
    ui->ByteStream->clear();
    ui->ByteStream->insertPlainText(displayStr);
} // SendvalueUpdated

/******************************************************************************
 * void SendIndexUpdated()
 * Updates the Tx Value based on the displayed index
 * ***************************************************************************/
void MainWindow::SendIndexUpdated(int value) {
    ui->Value->setValue((unsigned int) TxBuffer[value]);
} // SendIndexUpdated

/******************************************************************************
 * void ReadIndexUpdated()
 * pdates the Rx Value based on the displayed index
 * ***************************************************************************/
void MainWindow::ReadIndexUpdated(int value) {
    ui->ValueR->setValue((unsigned int) RxBuffer[value]);
} // ReadIndexUpdated

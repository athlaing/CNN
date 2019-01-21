#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "ftd2xx.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void InitializeWin();
public slots:
    // FPGA interfacing functions
    void ReadFromFPGA();
    void SendToFPGA();
    void InitializeFTDI();
    void CloseFTDI();
    // gui interfacing functions
    void DisplayTypeChanged(bool);
    void SendValueUpdated(int);
    void SendIndexUpdated(int);
    void ReadIndexUpdated(int);
private:
    Ui::MainWindow *ui;
    FT_HANDLE ftHandle; // handle for FTDI protocol
    unsigned char TxBuffer[256];
    unsigned char RxBuffer[256];
};

#endif // MAINWINDOW_H

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
    void InitializeFTDI();
public slots:
    void ReadFromFPGA();
    void SendToFPGA();
private:
    Ui::MainWindow *ui;
    FT_HANDLE ftHandle; // handle for FTDI protocol
    char TxBuffer[256];
    char RxBuffer[256];
};

#endif // MAINWINDOW_H

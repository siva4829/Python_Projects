import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, \
    QHBoxLayout, QStatusBar
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Application")
        self.setGeometry(300, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.label = QLabel("Weather Application", central_widget)
        self.line_edit = QLineEdit(central_widget)
        self.search_btn = QPushButton("Search", central_widget)
        self.temperature= QLabel("Temperature", central_widget)
        self.temperature_value = QLabel( central_widget)
        self.weather_status = QLabel("Weather Status", central_widget)
        self.weather_info = QLabel(central_widget)

        self.initUI()

    def initUI(self):
        self.label.setAlignment(Qt.AlignHCenter)
        central_widget = self.centralWidget()
        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        central_widget.setLayout(hbox)

        self.line_edit.setPlaceholderText("Miami")
        self.line_edit.setGeometry(150,70,300,50)
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.search_btn.setGeometry(230,125,120,50)
        self.temperature.setGeometry(215,170,200,80)
        self.temperature_value.setGeometry(260,240,150,50)
        self.weather_status.setGeometry(240,270,100,50)
        self.weather_info.setGeometry(220,310,300,50)

        #assign id
        self.label.setObjectName('label')
        self.line_edit.setObjectName('lineEdit')
        self.search_btn.setObjectName('searchBtn')
        self.temperature.setObjectName('temperature')
        self.temperature_value.setObjectName('temperatureValue')
        self.weather_status.setObjectName('weather_status')
        self.weather_info.setObjectName('weather_info')

        #stylesheet
        self.setStyleSheet("""
        #label{
        font-size:30px;
        font-weight:bold;
        font-style:italic;
        font-family:Arial;
        }
        #lineEdit{
        background-color:white;
        border : 3px solid black;
        border-radius:25px;
        font-size:20px;
        font-family:Arial;
        }
        #searchBtn{
        background-color:red;
        border : 3px solid black;
        border-radius:25px;
        font-size:20px;
        font-family:Arial;
        font-weight:bold;
        }
        #temperature{
        font-size:25px;
        font-weight:bold;
        font-family:Arial;
        }
        #temperatureValue{
        font-size:25px;
        font-family:Arial;
        }
        #weather_status{
        font-size:25px;
        font-weight:bold;
        font-family:Arial;
        }
        #weather_info{
        font-size:25px;
        font-family:Arial;
        }
    
        """
        )

        self.search_btn.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key=""  # PLEASE ENTER YOUR openweathermap API
        city=self.line_edit.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"]==200:
                self.display(data)

        except requests.exceptions.HTTPError as e:
            match response.status_code:
                case 400:
                    self.errors("Bad Request \nPlease check your input")
                case 401:
                    self.errors("Unauthorized \n Invalid API Key")
                case 403:
                    self.errors("Forbidden \n Access Denied")
                case 404:
                    self.errors("Not Found \n City Not Found")
                case 500:
                    self.errors("Internal Server Error \n Please try again later")
                case 502:
                    self.errors("Bad Gateway \n Invalid response from Server")
                case 503:
                    self.errors("Service Unavailable \n Service is down")
                case 504:
                    self.errors("Gateway Timeout \n No response from server")
                case _:
                    self.errors(f"HTTP Error Occured{e}")

        except requests.exceptions.RequestException as f:
            self.errors(f"request exception {f}")

        except requests.exceptions.ConnectionError:
            self.errors("Connection Error \n Check your internet connection")

        except requests.exceptions.Timeout:
            self.errors("Timeout Error \n Request Timed out")

        except requests.exceptions.TooManyRedirects:
            self.errors("TooManyRedirects Error \n Check the URL")



    def errors(self,message):

        self.temperature_value.clear()
        self.weather_status.clear()
        self.weather_info.clear()
        self.temperature.setText(message)


    def display(self,data):
        self.temperature.setText("Temperature")
        self.weather_status.setText("Weather Status")
        temperature_kelvin = data["main"]["temp"]
        temperature_celsius = temperature_kelvin
        self.temperature_value.setText(f"{temperature_celsius:.0f}°C")
        discription = data["weather"][0]["description"]
        self.weather_info.setText(discription)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

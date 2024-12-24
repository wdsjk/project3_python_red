import dash

from flask import Flask, request, render_template

from DashManager import DashManager
from WeatherManager import WeatherManager

server = Flask(__name__)
dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

API_KEY = ""
weather_manager = WeatherManager(API_KEY)
dash_manager = DashManager()

dash_app.layout = dash_manager.create_dash_layout

@server.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_location = request.form['start']
        locations = request.form['intermediate'].replace(' ', '').split(',')
        end_location = request.form['end']
        interval = int(request.form['interval'])

        try:
            weather_data = {start_location: weather_manager.get_weather_data(start_location, interval)}
            dates_list = list(weather_data[start_location][1].keys())

            for location in locations:
                if location:
                    weather_data[location] = weather_manager.get_weather_data(location, interval)
            weather_data[end_location] = weather_manager.get_weather_data(end_location, interval)

            dash_app.layout = dash_manager.create_dash_layout(weather_data, interval, dates_list)
            return dash_app.index()

        except Exception as e:
            print(f'Произошла ошибка: {e}')
            return render_template('exception.html', error=e)

    return render_template('index.html')


def main():
    server.run(debug=True)


if __name__ == '__main__':
    main()

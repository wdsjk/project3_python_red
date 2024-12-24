from dash import dcc, html
import plotly.graph_objs as go


class DashManager:
    def __init__(self):
        pass

    @staticmethod
    def create_map(weather_data, dates_list):
        fig = go.Figure()

        if weather_data:
            cities = list(weather_data.keys())
            city_coords = {}

            for city in cities:
                city_coords[city] = weather_data[city][0]

            lat_list = [weather_data[city][0][0] for city in cities]
            lon_list = [weather_data[city][0][1] for city in cities]

            hover_texts = []
            for city in cities:
                temperature = []
                wind_speed = []
                precipitation = []

                for date in dates_list:
                    temperature.append(f"{weather_data[city][1][date].get('temperature', 'N/A')}°C")
                    wind_speed.append(f"{weather_data[city][1][date].get('wind_speed', 'N/A')} м/с")
                    precipitation.append(weather_data[city][1][date].get('precipitation', 'N/A'))

                hover_texts.append(
                    f"{city}<br>Температура: {', '.join(temperature)}<br>Скорость ветра: {', '.join(wind_speed)}<br>Состояние: {precipitation}"
                )

            fig.add_trace(go.Scattermapbox(
                lat=lat_list,
                lon=lon_list,
                mode='markers+lines',
                marker=go.scattermapbox.Marker(size=10, color="blue"),
                text=hover_texts,
                hoverinfo='text',
                name="Маршрут"
            ))

            fig.update_layout(
                mapbox=dict(
                    style="open-street-map",
                    zoom=3,
                    center={"lat": sum(lat_list) / len(lat_list),
                            "lon": sum(lon_list) / len(lon_list)}
                ),
                title="Маршрут на карте"
            )

        return fig

    @staticmethod
    def create_temperature_graph(weather_data, interval):
        figure = go.Figure()

        if weather_data:
            for city, data in weather_data.items():
                data = data[1]
                if interval == 1:
                    figure.add_trace(go.Bar(
                        x=list(data.keys()),
                        y=[day_data['temperature'] for day_data in data.values()],
                        name=f'Температура в {city}'
                    ))
                else:
                    figure.add_trace(go.Scatter(
                        x=list(data.keys()),
                        y=[day_data['temperature'] for day_data in data.values()],
                        mode='lines+markers',
                        name=f'Температура в {city}'
                    ))

        figure.update_layout(title="Температура",
                             xaxis_title='День',
                             yaxis_title='Температура (°C)',
                             template='plotly')

        return figure

    @staticmethod
    def create_wind_speed_graph(weather_data, interval):
        figure = go.Figure()

        if weather_data:
            for city, data in weather_data.items():
                data = data[1]
                if interval == 1:
                    figure.add_trace(go.Bar(
                        x=list(data.keys()),
                        y=[day_data['wind_speed'] for day_data in data.values()],
                        name=f'Скорость ветра в {city}'
                    ))
                else:
                    figure.add_trace(go.Scatter(
                        x=list(data.keys()),
                        y=[day_data['wind_speed'] for day_data in data.values()],
                        mode='lines+markers',
                        name=f'Скорость ветра в {city}'
                    ))

        figure.update_layout(title="Скорость ветра",
                             xaxis_title='День',
                             yaxis_title='Скорость ветра (м/с)',
                             template='plotly')

        return figure

    @staticmethod
    def create_precipitation_graph(weather_data: dict):
        state_counts = {}

        if weather_data:
            cities = weather_data.keys()

            for city in cities:
                state_counts[city] = {}

            for city, data in weather_data.items():
                data = data[1]
                for day in data.values():
                    states = day.get('precipitation', [])
                    if isinstance(states, list):
                        for state in states:
                            state_counts[city][state] = state_counts[city].get(state, 0) + 1
                    else:
                        state_counts[city][states] = state_counts[city].get(states, 0) + 1

        figure = go.Figure()

        for city, states in state_counts.items():
            states_list = list(states.keys())
            counts_list = list(states.values())
            figure.add_trace(go.Bar(
                x=states_list,
                y=counts_list,
                name=city
            ))

        figure.update_layout(title="Количество дней с состояниями погоды по городам",
                             xaxis_title='Состояние погоды',
                             yaxis_title='Количество дней',
                             template='plotly',
                             barmode='group')

        return figure

    def create_dash_layout(self, weather_data=None, interval=1, dates_list=None):
        layout = html.Div([
            dcc.Store(id='weather-data', data=weather_data),
            html.H1("Прогноз погоды"),

            dcc.Graph(id='map-graph', figure=self.create_map(weather_data, dates_list)),
            dcc.Graph(id='temperature-graph', figure=self.create_temperature_graph(weather_data, interval)),
            dcc.Graph(id='wind-speed-graph', figure=self.create_wind_speed_graph(weather_data, interval)),
            dcc.Graph(id='precipitation-graph', figure=self.create_precipitation_graph(weather_data)),
            html.A("Назад", href='/', className='btn-custom'),
        ])
        return layout


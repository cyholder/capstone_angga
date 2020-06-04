from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64
import matplotlib


matplotlib.use('Agg')


from helper import load_telco, table_churn, plot_phone, plot_internet, plot_tenure_cltv, plot_tenure_churn, plot_arpu_internet_tenure, plot_arpu_phone_tenure

from helper import plot_arpu_phone_single, plot_arpu_phone_multi, plot_arpu_inet_fo

from helper import plot_arpu_dsl


app = Flask(__name__)

data = load_telco()

@app.route("/")
def index():
	# copy data as raw
	raw = data.copy()

	# generate value for cards
	## churn rate & retaining customers
	table_churn_res = table_churn(raw)
	percent_churn = table_churn_res.loc['Yes', 'percent'].round(2)
	percent_retain = table_churn_res.loc['No', 'percent'].round(2)
	## average lifetime value
	average_cltv = int(data['cltv'].mean())
	# compile card values as `card_data`
	card_data = dict(
			percent_churn = f'{percent_churn}%',
			percent_retain = f'{percent_retain}%',
			average_cltv = f'{average_cltv:,}'
		)

	# generate plot
	plot_phone_res = plot_phone(raw)
	plot_internet_res = plot_internet(raw)
	plot_tenure_cltv_res = plot_tenure_cltv(raw)
	plot_tenure_churn_res = plot_tenure_churn(raw)
	plot_arpu_internet_tenure_res = plot_arpu_internet_tenure(raw)
	plot_arpu_phone_tenure_res = plot_arpu_phone_tenure(raw)
	plot_arpu_phone_single_res = plot_arpu_phone_single(raw)
	plot_arpu_phone_multi_res = plot_arpu_phone_multi(raw)
	plot_arpu_inet_fo_res = plot_arpu_inet_fo(raw)
	plot_arpu_dsl_res = plot_arpu_dsl(raw)

	# render to html
	return render_template('index.html',
			card_data = card_data, 
			plot_phone_res=plot_phone_res,
			plot_internet_res=plot_internet_res,
			plot_tenure_cltv_res=plot_tenure_cltv_res,
			plot_tenure_churn_res=plot_tenure_churn_res,
			plot_arpu_internet_tenure_res = plot_arpu_internet_tenure_res,
			plot_arpu_phone_tenure_res = plot_arpu_phone_tenure_res,
			plot_arpu_phone_single_res = plot_arpu_phone_single_res,
			plot_arpu_phone_multi_res = plot_arpu_phone_multi_res,
			plot_arpu_inet_fo_res = plot_arpu_inet_fo_res,
			plot_arpu_dsl_res = plot_arpu_dsl_res
		)


if __name__ == "__main__": 
    app.run(debug=True)

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dat = yf.download('GOLD', period='3y', auto_adjust=True)

open_p = dat['Open'].iloc[:, 0]
tutup = dat['Close'].iloc[:, 0]
high_p = dat['High'].iloc[:, 0]
low_p = dat['Low'].iloc[:, 0]
vol_p = dat['Volume'].iloc[:, 0]
base = 10000

log_harga = np.log(tutup)
ret = log_harga - log_harga.shift(1)
fair_value = tutup.rolling(20, closed='left').mean()
hell_nah = tutup.rolling(40, min_periods=35, closed='left').std()
anom_bottom = fair_value - (2 * hell_nah)
anom_top = fair_value + (2 * hell_nah)
buy_trig = open_p <= anom_bottom
close_trig = open_p >= fair_value


realized_vol = ret.rolling(120, closed='left').std() * np.sqrt(252)
target_vol = 0.15
bobot_mentah = target_vol / realized_vol
bobot_efektif = bobot_mentah.clip(0.1, 1.2)

raw_signal = np.where(buy_trig, 1.0, np.where(close_trig, 0.0, np.nan))
status_posisi = pd.Series(raw_signal, index=tutup.index).ffill().fillna(0.0)
posisi_aktif = status_posisi.shift(1).fillna(0.0)
posisi_final = posisi_aktif * bobot_efektif
strategy_ret = posisi_final * ret
equity_curve = np.exp(strategy_ret.cumsum())

plt.figure(figsize=(12, 6))
plt.plot(equity_curve, label='equity curve (vol-targeted mean reversion)', color='darkgoldenrod', lw=1.5)
plt.title('simulation growing strategy (anti bias and vol targeting)', fontsize=12)
plt.xlabel('date')
plt.ylabel('growing base cumulative (base = 1.0)')
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()
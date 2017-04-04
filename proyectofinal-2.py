import tensorflow as tf
import pandas as pd
import numpy as np
import tempfile
import time
import sys

global numeroModelo

if int(sys.argv[1]) == 1:
	numeroModelo = str("1")
elif int(sys.argv[1]) == 2:
	numeroModelo = str("2")
elif int(sys.argv[1]) == 3:
	numeroModelo = str("3")
else:
	print("Sólo se puede correr con números entre el 1, 2 o 3. \n")
	exit()

iteraciones = int(sys.argv[2])

alpha = float(sys.argv[3])

# Evita que salgan warnings propios de tensorflow
tf.logging.set_verbosity(tf.logging.ERROR)
# Aqui se crean los archivos de train y test

def dividirDataset(nombre):
	train = str("train_set-" + numeroModelo + ".csv")
	test = str("test_set-" + numeroModelo + ".csv")
	pred = str("pred_set-" + numeroModelo + ".csv")
	train_set = open(train, 'w')
	test_set = open(test, 'w')
	lines = open(nombre, 'r').readlines()
	header = lines[0]
	lines = lines[1:]
	np.random.shuffle(lines)
	corte = int((len(lines) - 1) * 80 / 100)
	i = 1
	train_set.write(header)
	test_set.write(header)
	for line in lines:
		if i <= corte:
			train_set.write(line)
		else:
			test_set.write(line)
		i += 1
	train_set.close()
	test_set.close()

	return train, test, pred

nombre = str("dataset-"+ numeroModelo + ".csv")
train, test, pred = dividirDataset(nombre)

COLUMNS = ["year1", "year2", "playerID", "wins_games", "losses_games", "outs_pitched", 
			"earned_runs", "strike_outs_outs_pitched", "walks_outs_pitched", "opponent_batting_avg", 
			"league_batting_avg","earned_run_avg_year1", "earned_run_avg_year2"]

CONTINUOUS_COLUMNS = ["wins_games", "losses_games", "outs_pitched", "earned_runs", 
						"strike_outs_outs_pitched", "walks_outs_pitched", "opponent_batting_avg",
						"league_batting_avg","earned_run_avg_year1"]

LABEL_COLUMN = "label"
df_train = pd.read_csv(train, names=COLUMNS, skipinitialspace=True, skiprows=1)
df_test = pd.read_csv(test, names=COLUMNS, skipinitialspace=True, skiprows=1)
df_pred = pd.read_csv(pred, names=COLUMNS, skipinitialspace=True, skiprows=1)

df_train[LABEL_COLUMN] = df_train["earned_run_avg_year2"]
df_test[LABEL_COLUMN] = df_test["earned_run_avg_year2"]
df_pred[LABEL_COLUMN] = df_pred["earned_run_avg_year2"]

# Declaracion de funcion que permite la creacion del tensor que va a tener los datos para entrenar y evaluar
def input_fn(df):
	feature_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
	label = tf.constant(df["earned_run_avg_year2"].values)
	return feature_cols, label

def train_input_fn():
	return input_fn(df_train)

def eval_input_fn():
	return input_fn(df_test)

def pred_input_fn():
	return input_fn(df_pred)

def predicciones(dataset, resultados, error, salida, boolean):
	salida = open(salida, 'w')
	for key in sorted(error):
		linea = "{0}: {1} \n".format(key, error[key])
		salida.write(linea)

	aux = 0
	for i in resultados:
		linea = "Jugador: {0} | Año: {1} | Prediccion: {2}".format(dataset["playerID"][aux],dataset["year2"][aux],i)
		if boolean:
			linea += " | Verdadero: {0} \n".format(dataset[LABEL_COLUMN][aux])
		else:
			linea += " \n"
		salida.write(linea)
		aux += 1

	salida.close()

def main():
	
	tf.reset_default_graph()

	# Carpeta donde se guardaran los modelos creados
	model_dir = str("modelo-" + numeroModelo)
	
	# Declaracion de los tensores de los atributos a usarse
	wins_games = tf.contrib.layers.real_valued_column("wins_games")
	losses_games = tf.contrib.layers.real_valued_column("losses_games")
	outs_pitched = tf.contrib.layers.real_valued_column("outs_pitched")
	earned_runs = tf.contrib.layers.real_valued_column("earned_runs")
	strike_outs_outs_pitched = tf.contrib.layers.real_valued_column("strike_outs_outs_pitched")
	walks_outs_pitched = tf.contrib.layers.real_valued_column("walks_outs_pitched")
	opponent_batting_avg = tf.contrib.layers.real_valued_column("opponent_batting_avg")
	league_batting_avg = tf.contrib.layers.real_valued_column("league_batting_avg")
	earned_run_avg_year1 = tf.contrib.layers.real_valued_column("earned_run_avg_year1")

	# Declaracion de modelo a usar
	m = tf.contrib.learn.LinearRegressor(feature_columns=[wins_games, losses_games, outs_pitched, earned_runs,
			strike_outs_outs_pitched, walks_outs_pitched, opponent_batting_avg, league_batting_avg, earned_run_avg_year1], 
			optimizer=tf.train.FtrlOptimizer(learning_rate=alpha, l1_regularization_strength=1, 
			l2_regularization_strength=1), model_dir=model_dir)

	start = time.time()
	# Entrenamiento del modelo
	m.fit(input_fn=train_input_fn, steps=iteraciones)
	total = time.time() - start
	print("Duración de entrenamiento: {0} segundos \n".format(total))
	
	# Evaluacion del modelo entrenado, se obtiene el error (MSE)
	error = m.evaluate(input_fn=eval_input_fn, steps=1)
	comparison = m.predict(input_fn=eval_input_fn)

	# Se pasan determinadas instancias y se le pasan al modelo para realizar una prediccion
	predicciones2016 = m.predict(input_fn=pred_input_fn)

	salida1 = str("comparacion-"+ numeroModelo + ".txt")
	predicciones(df_test, comparison, error, salida1, True)

	#salida2 = str("prediccion2016-"+ numeroModelo + ".txt")
	#predicciones(df_pred, predicciones2016, error, salida2, False)

	test_writer = tf.summary.FileWriter(model_dir)

if __name__ == '__main__':
	main()
# lavh @ 12:08 2/7/2023

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import tensorflow as tf

from tensorflow import keras


# Dense Neural Network
class RankingModel:
    dataset = pd.DataFrame()


def read_in(ranker):
    filename = input("Input training filename")
    ranker.dataset = pd.read_csv(filename)


def plot_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Error [Round or Rank]')
    plt.legend()
    plt.grid(True)


def train(Ranker):
    # read into the Ranker dataframe
    read_in(Ranker)

    # drop Num, Rk, Team, Conf, W-L
    Ranker.dataset = Ranker.dataset.drop(['Num', 'Rk', 'Team', 'Conf', 'W-L', 'Round'], axis=1)

    # drop teams without stats, or not in tournament
    Ranker.dataset = Ranker.dataset.dropna()

    # set up training and testing datasets
    train_dataset = Ranker.dataset.sample(frac=0.8, random_state=0)
    test_dataset = Ranker.dataset.drop(train_dataset.index)

    # inspect data of base stats that impact tournament success
    inspection = input("Do you want to inspect the data? (y/n/l)")
    if inspection == 'y':
        # first input is the result of the function
        # AdjEM	AdjO	AdjD	AdjT	Luck	AdjEM.1	OppO	OppD	AdjEM.2	FG	FGA	FGpct	2PT	2PTA	2PTpct	3PT	3PTA	3PTpct	FT	FTA	FTpct	ORB	DRB	TRB	AST	STL	BLK	TOV	PF	PTS	FG_RANK	FGA_RANK	FGpct_RANK	2PT_RANK	2PTA_RANK	2PTpct_RANK	3PT_RANK	3PTA_RANK	3PTpct_RANK	FT_RANK	FTA_RANK	FTpct_RANK	ORB_RANK	DRB_RANK	TRB_RANK	AST_RANK	STL_RANK	BLK_RANK	TOV_RANK	PF_RANK	PTS_RANK	OPP_FG	OPP_FGA	OPP_FGpct	OPP_2PT	OPP_2PTA	OPP_2PTpct	OPP_3PT	OPP_3PTA	OPP_3PTpct	OPP_FT	OPP_FTA	OPP_FTpct	OPP_ORB	OPP_DRB	OPP_TRB	OPP_AST	OPP_STL	OPP_BLK	OPP_TOV	OPP_PF	OPP_PTS	OPP_FG_RANK	OPP_FGA_RANK	OPP_FGpct_RANK	OPP_2PT_RANK	OPP_2PTA_RANK	OPP_2PTpct_RANK	OPP_3PT_RANK	OPP_3PTA_RANK	OPP_3PTpct_RANK	OPP_FT_RANK	OPP_FTA_RANK	OPP_FTpct_RANK	OPP_ORB_RANK	OPP_DRB_RANK	OPP_TRB_RANK	OPP_AST_RANK	OPP_STL_RANK	OPP_BLK_RANK	OPP_TOV_RANK	OPP_PF_RANK	OPP_PTS_RANK
        sns.pairplot(train_dataset[['Round', 'AdjEM', 'AdjD', 'AdjT']], diag_kind='kde')
        train_dataset.describe().transpose()

    # separating labels from features
    train_features = train_dataset.copy()
    test_features = test_dataset.copy()
    train_labels = train_features.pop('Rank')
    test_labels = test_features.pop('Rank')

    # converting to floats
    train_features = np.asarray(train_features).astype('float32')
    test_features = np.asarray(test_features).astype('float32')

    if inspection == 'y':
        train_dataset.describe().transpose()[['mean', 'std']]

    # setup normalizing layer
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(np.array(train_features))

    # expand the dimensions of the data
    train_features = tf.expand_dims(train_features, axis=-1)
    test_features = tf.expand_dims(test_features, axis=-1)
    train_labels = tf.expand_dims(train_labels, axis=-1)
    test_labels = tf.expand_dims(test_labels, axis=-1)
    train_labels = tf.expand_dims(train_labels, axis=-1)
    test_labels = tf.expand_dims(test_labels, axis=-1)

    if inspection == 'y':
        print(normalizer.mean.numpy())

        first = np.array(train_features[:1])

        with np.printoptions(precision=2, suppress=True):
            print('First example:', first)
            print()
            print('Normalized:', normalizer(first).numpy())

    model = keras.Sequential([
        normalizer,
        keras.layers.Dropout(0.4),
        keras.layers.Dense(175, activation='tanh'),
        keras.layers.Dense(200, activation='elu',
            kernel_initializer='ones',
            kernel_regularizer=tf.keras.regularizers.L1(0.01),
            activity_regularizer=tf.keras.regularizers.L2(0.01)),
        keras.layers.Dense(138, activation='elu',
            kernel_initializer='ones',
            kernel_regularizer=tf.keras.regularizers.L1(0.01),
            activity_regularizer=tf.keras.regularizers.L2(0.01)),
        keras.layers.Dense(156, activation='selu',
            kernel_initializer='lecun_normal'),
        keras.layers.Dense(156, activation= 'elu'),
        keras.layers.Dense(1)
    ])

    model.compile(loss='mean_absolute_error',
                  optimizer=tf.keras.optimizers.Nadam(learning_rate=0.00006))

    if inspection == 'y':
        model.summary()

    # training the model
    history = model.fit(
        train_features,
        train_labels,
        validation_split=0.2,
        verbose=0, epochs=1600, batch_size=64)

    if inspection == 'y':
        plot_loss(history)

    if inspection == 'l':
        plot_loss(history)

    history2 = model.fit(
        train_features,
        train_labels,
        validation_data=(test_features, test_labels),
        verbose=0, epochs=2500, batch_size=64)

    if inspection == 'y':
        plot_loss(history2)

    if inspection == 'l':
        plot_loss(history2)

    # results to evaluate with
    results = model.evaluate(test_features, test_labels, verbose=0)

    if inspection == 'y':
        print(results)

    if inspection == 'l':
        print(results)

    # PREDICT

    # read in ranking file
    file = input("File to rank")
    csv = pd.read_csv(file)
    teams = csv.pop('Team')
    csv = csv.drop(['Num', 'Rk', 'Conf', 'W-L'], axis=1)
    csv = csv.dropna()

    # converting to floats
    csv = np.asarray(csv).astype('float32')

    # predict using model
    results = model.predict(csv)

    # combine the rankings with their respective teams and sort
    rdf = pd.DataFrame(results, columns=['results'])
    output = pd.concat([teams, rdf], axis=1)
    output.sort_values(by=['results'])

    # print out results of the model
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        print(output)


def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    Ranker = RankingModel()
    train(Ranker)


if __name__ == '__main__':
    main()

# lavh @ 12:08 2/7/2023

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import tensorflow as tf

from tensorflow import keras


class RankingModel:
    dataset = pd.DataFrame()
    model = keras.Sequential()

    def build_and_compile_model(norm):
        model = keras.Sequential([
            norm,
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(1)
        ])

        model.compile(loss='mean_absolute_error',
                      optimizer=tf.keras.optimizers.Adam(0.001))


def read_in(ranker):
    filename = input("Input training filename")
    ranker.dataset = pd.read_csv(filename)


def plot_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.ylim([0, 10])
    plt.xlabel('Epoch')
    plt.ylabel('Error [MPG]')
    plt.legend()
    plt.grid(True)


def train(Ranker):
    # read into the Ranker dataframe
    read_in(Ranker)

    # drop teams without stats, or not in tournament
    Ranker.dataset = Ranker.dataset.dropna()

    # set up training and testing datasets
    train_dataset = Ranker.dataset.sample(frac=0.8, random_state=0)
    test_dataset = Ranker.dataset.drop(train_dataset.index)

    # inspect data of base stats that impact tournament success
    inspection = input("Do you want to inspect the data?")
    if inspection == 'yes':
        # first one is the result of the function
        sns.pairplot(train_dataset[['Round', 'PPG', 'MOV', 'Weight']], diag_kind='kde')
        train_dataset.describe().transpose()

    # separating labels from features
    train_features = train_dataset.copy()
    test_features = test_dataset.copy()
    train_labels = train_features.pop('Round')
    test_labels = test_features.pop('Round')

    if inspection == 'yes':
        train_dataset.describe().transpose()[['mean', 'std']]

    # setup normalizing layer
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(np.array(train_features))

    if inspection == 'yes':
        print(normalizer.mean.numpy())

        first = np.array(train_features[:1])

        with np.printoptions(precision=2, suppress=True):
            print('First example:', first)
            print()
            print('Normalized:', normalizer(first).numpy())

    Ranker.build_and_compile_model(normalizer)

    if inspection == 'yes':
        Ranker.model.summary()

    # training the model
    history = Ranker.model.fit(
        train_features,
        train_labels,
        validation_split=0.2,
        verbose=0, epochs=100)

    if inspection == 'yes':
        plot_loss(history)

    # results to evaluate with
    results = Ranker.model.evaluate(test_features, test_labels, verbose=0)

    if inspection == 'yes':
        print(results)


def predict(Ranker):
    # read in ranking file
    file = input("File to rank")
    csv = pd.read_csv(file)
    teams = csv['Teams']

    # predict using model
    results = Ranker.model.predict(csv)

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
    predict(Ranker)


if __name__ == '__main__':
    main()

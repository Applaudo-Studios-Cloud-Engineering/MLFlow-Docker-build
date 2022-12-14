from kfp.v2.dsl import component, Dataset, OutputPath, InputPath

@component(
    packages_to_install=['pandas', 'numpy', 'fsspec', 'gcsfs', 'tensorflow']
)
def preprocess(path_train:str, path_test:str, y_train: OutputPath(Dataset), x_train: OutputPath(), x_test: OutputPath()):

    import pandas as pd
    import numpy as np
    import tensorflow as tf
    from tensorflow.python.lib.io import file_io
    from numpy import asarray
    from numpy import savetxt

    train_df = pd.read_csv(path_train)
    test_df = pd.read_csv(path_test)

    Y_train = train_df['label'].astype('float32')
    X_train = train_df.drop(['label'], axis=1).astype('int32')
    X_test = test_df.astype('float32') 

    Y_train.to_csv(y_train, index=False)

    sample_count = []
    for i in range(0,10):
        curr_count = train_df['label'][train_df['label'] == i].count()
        sample_count.append((i, curr_count))

        print(f'Training samples of digit {i} ', curr_count)


    sample_count_df = pd.DataFrame(sample_count, columns=['digit', 'count'])
    sample_count_df.head()
    print(sample_count_df)

    X_train = X_train/255
    X_test = X_test/255

    X_train = X_train.values.reshape(-1, 28, 28, 1)
    X_test = X_test.values.reshape(-1, 28, 28, 1)
    X_train.shape
    
    np.save(file_io.FileIO(x_train, 'w'), X_train)
    np.save(file_io.FileIO(x_test, 'w'), X_test)


@component(
    packages_to_install=['pandas', 'numpy', 'fsspec', 'gcsfs', 'tensorflow', 'mlflow'],
    base_image="python:3.9"
)
def model_create(
        y: InputPath(Dataset), 
        x: InputPath(), 
        test: InputPath(), 
        model_path: OutputPath()
    ):
    import tensorflow as tf
    import pandas as pd
    import numpy as np
    import mlflow
    from mlflow.models.signature import infer_signature
    from tensorflow.python.lib.io import file_io
    from io import BytesIO

    mlflow.set_tracking_uri("http://my-mlflow.mlflow.svc.cluster.local:5000")
    mlflow.set_experiment(experiment_name="mnist")
    mlflow.set_registry_uri("http://my-mlflow.mlflow.svc.cluster.local:5000")
    
    mlflow.tensorflow.autolog(
        registered_model_name="tensorflow-model-mnist",
        log_input_examples=True,
        keras_model_kwargs = {'save_format': 'h5'} # works
    )

    Y_train = pd.read_csv(y)
    Y_train = tf.keras.utils.to_categorical(Y_train, num_classes=10)

    model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, kernel_size=(3,3), input_shape=(28, 28, 1), name='Conv_1', activation='relu'),
    tf.keras.layers.Conv2D(16, kernel_size=(3,3), padding='same', name='Conv_2', activation='relu'),
    tf.keras.layers.BatchNormalization(name='Batch_Norm_1'),
    tf.keras.layers.MaxPooling2D(name='Max_Pool_1'),
    tf.keras.layers.Dropout(0.2, name='Drop_1'),
    tf.keras.layers.Conv2D(32, kernel_size=(3,3), name='Conv_3', activation='relu'),
    tf.keras.layers.Conv2D(32, kernel_size=(3,3), padding='same', name='Conv_4', activation='relu'),
    tf.keras.layers.BatchNormalization(name='Batch_Norm_2'),
    tf.keras.layers.MaxPooling2D(name='Max_Pool_2'),
    tf.keras.layers.Dropout(0.25, name='Drop_2'),
    tf.keras.layers.Flatten(name='Flat_1'),
    tf.keras.layers.Dense(96, activation='relu', name='Dense_1'),
    tf.keras.layers.Dense(10, activation='softmax', name='Dense_2')
    ])

    model.compile(optimizer='Adam', loss='CategoricalCrossentropy', metrics='accuracy')

    model.summary()
    
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=0, patience=5)

    x_train_file = BytesIO(file_io.read_file_to_string(x, binary_mode=True))
    X_train = np.load(x_train_file)

    history = model.fit(X_train, Y_train, validation_split=0.2, epochs=80, callbacks=[early_stop])
    print(history)

    x_test_file = BytesIO(file_io.read_file_to_string(test, binary_mode=True))
    X_test = np.load(x_test_file)    

    y_hat = model.predict(X_test).argmax(axis=1)
    submission_df = pd.DataFrame({ 'ImageId': list(range(1, len(y_hat) + 1)), 'Label': y_hat})
    submission_df.head()

    # signature = infer_signature(X_train, Y_train)
    # model.save(model_path, save_format='h5',signatures=signature)

    mlflow.end_run()
import kfp
import kfp.dsl as dsl
from kfp import compiler
from nodes import preprocess, model_create

@dsl.pipeline(
    name = 'MNIST-pipeline',
    description = 'Test to create the pipeline',
    pipeline_root = 'gs://data-bucket-6929d24320ef4e55/dataTrain/mnist/build'
)
def add_pipeline(path_train: str = 'gs://data-bucket-6929d24320ef4e55/data/mnist/train.csv', path_test: str='gs://data-bucket-6929d24320ef4e55/data/mnist/test.csv'):
    data_preprocess = preprocess(path_train, path_test)
    model = model_create(data_preprocess.outputs['y_train'], data_preprocess.outputs['x_train'], data_preprocess.outputs['x_test']) 


compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(pipeline_func=add_pipeline, package_path='pipeline.yaml')
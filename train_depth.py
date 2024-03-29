from models.fpn_depth import FpnDepth
from trainers.segmentation_trainer import SegmentationTrainer
from data_generators.depth_data_generator import DepthDataGenerator
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args
import tensorflow as tf
from tensorflow.keras.mixed_precision import experimental as mixed_precision


def main():
        # capture the config path from the run arguments
        # then process the json configuration file
    try:
        args = get_args()
        config = process_config(args.config)
    except:
        print("missing or invalid arguments")
        exit(0)

    # use mixed precision for training
    if config.exp.mixed_precision:
        print('Use mixed precision training')
        policy = mixed_precision.Policy('mixed_float16')
        mixed_precision.set_policy(policy)

    if config.exp.jpa_optimization:
        tf.config.optimizer.set_jit(True)

    # create the experiments dirs
    create_dirs([config.callbacks.tensorboard_log_dir,
                 config.callbacks.checkpoint_dir])

    print('Create the training data generator.')
    train_data = DepthDataGenerator(config)

    validation_data = None
    if type(config.validation.img_dir) == str:
        print('Create the validation data generator.')
        validation_data = DepthDataGenerator(
            config, is_training_set=False)

    print('Create the model.')
    model = FpnDepth(config, train_data)

    print('Create the trainer')
    trainer = SegmentationTrainer(
        model, train_data, config, validation_generator=validation_data)

    print('Start training the model.')
    trainer.train()


if __name__ == '__main__':
    main()

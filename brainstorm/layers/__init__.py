#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function
from functools import partial
import sys
from brainstorm.utils import get_inheritors
from brainstorm.structure.construction import ConstructionWrapper

# need to import every layer implementation here
from brainstorm.layers.base_layer import LayerBaseImpl
from brainstorm.layers.input_layer import InputLayerImpl
from brainstorm.layers.noop_layer import NoOpLayerImpl
from brainstorm.layers.fully_connected_layer import FullyConnectedLayerImpl
from brainstorm.layers.squared_difference_layer import \
    SquaredDifferenceLayerImpl
from brainstorm.layers.binomial_cross_entropy_layer import \
    BinomialCrossEntropyLayerImpl
from brainstorm.layers.classification_layer import ClassificationLayerImpl
from brainstorm.layers.loss_layer import LossLayerImpl


CONSTRUCTION_LAYERS = {}

# ---------------- Specialized Construction Layers ----------------------------
# defined explicitly to provide improved autocompletion


def InputLayer(out_shapes, name=None):
    return ConstructionWrapper.create('InputLayer',
                                      name=name,
                                      out_shapes=out_shapes)


def FullyConnectedLayer(shape, activation_function='linear', name=None):
    return ConstructionWrapper.create('FullyConnectedLayer',
                                      shape=shape,
                                      name=name,
                                      activation_function=activation_function)


def LossLayer(name=None):
    return ConstructionWrapper.create('LossLayer', name=name)


def BinomialCrossEntropyLayer(name=None):
    return ConstructionWrapper.create('BinomialCrossEntropyLayer',
                                      name=name)


def ClassificationLayer(shape, name=None):
    return ConstructionWrapper.create('ClassificationLayer',
                                      shape=shape,
                                      name=name)


def SquaredDifferenceLayer(name=None):
    return ConstructionWrapper.create('SquaredDifferenceLayer',
                                      name=name)


# ------------------------ Automatic Construction Layers ----------------------

def construction_layer_for(layer_impl):
    layer_name = layer_impl.__name__
    assert layer_name.endswith('Impl'), \
        "{} should end with 'Impl'".format(layer_name)
    layer_name = layer_name[:-4]
    return partial(ConstructionWrapper.create, layer_name)


for Layer in get_inheritors(LayerBaseImpl):
    layer_name = Layer.__name__[:-4]
    if layer_name not in CONSTRUCTION_LAYERS:
        CONSTRUCTION_LAYERS[layer_name] = construction_layer_for(Layer)


this_module = sys.modules[__name__]  # this module
for name, cl in CONSTRUCTION_LAYERS.items():
    if not hasattr(this_module, name):
        setattr(this_module, name, cl)



# somehow str is needed because in __all__ unicode does not work
__all__ = ['construction_layer_for'] + [str(a) for a in CONSTRUCTION_LAYERS]

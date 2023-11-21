from optparse import OptionParser

parser = OptionParser()
parser.add_option("--formatting", default="psplib",
                  action="store", type="string", dest="formatting",
                  help="format: psplib,...")
parser.add_option("--mode", default="learning",
                  action="store", type="string", dest="mode",
                  help="mode: 'learning', 'evaluation', 'prediction'")
parser.add_option("--split-id", default="0",
                  action="store", type="string", dest="split_tag",
                  help="id of the general split used, default '0'", metavar="STR")
parser.add_option("--split-cross-id", default="0",
                  action="store", type="string", dest="split_cross_tag",
                  help="id of the instance split used, default '0'", metavar="STR")
parser.add_option("--cross-type", default="uniform",
                  action="store", type="string", dest="cross_type",
                  help="uniform or balanced, default 'uniform'", metavar="STR")
parser.add_option("--kcross", default="0",
                  action="store", type=int, dest="kcross",
                  help="id of the cross validation section")
parser.add_option("--psplib", default="<=j60",
                  action="store", type="string", dest="psplib_batch",
                  help="instances sizes to work on")
parser.add_option("--psplib-graph", default="j301_1",
                  action="store", type="string", dest="psplib_graph",
                  help="name of the graph to do a prediction")
parser.add_option("--subbatch", default="unseen",
                  action="store", type="string", dest="subbatch",
                  help="Subset of the instances: 'seen', 'unseen', 'unknown' or 'all'")
parser.add_option("--epoch", default=100,
                  action="store", type=int, dest="epoch",
                  help="epoch for the learning")
parser.add_option("--lr", default=0.01,
                  action="store", type=float, dest="learning_rate",
                  help="learning rate for the optimizer")
parser.add_option("--ds-opts", default="TO=1000_sbps=false_vsids=false",
                  action="store", type="string", dest="dataset_opts",
                  help="id of the input dataset")
parser.add_option("--model-name", default="",
                  action="store", type="string", dest="model_name",
                  help="name of the model to use")





if __name__ == "__main__":
    (options, args) = parser.parse_args()
    print('test')
    print(options)

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--psplib-graph", default="j301_1",
                  action="store", type="string", dest="psplib_graph",
                  help="name of the graph to do a prediction")
parser.add_option("--model-name", default="",
                  action="store", type="string", dest="model_name",
                  help="name of the model to use")
parser.add_option("--threshold", default=0.55,
                  action="store", type=float, dest="threshold",
                  help="threshold to filter")
parser.add_option("--ls-keep", default=0.15,
                  action="store", type=float, dest="ls_keep",
                  help="threshold to filter")

parser.add_option("--vsids", default="true",
                  action="store", type="string", dest="vsids",
                  help="threshold to filter")
parser.add_option("--sbps", default="true",
                  action="store", type="string", dest="sbps",
                  help="threshold to filter")

parser.add_option("--to-total", default=600000,
                  action="store", type=int, dest="to_total",
                  help="time out for the whole execution")
parser.add_option("--to-round", default=120000,
                  action="store", type=int, dest="to_round",
                  help="time out for one loop")
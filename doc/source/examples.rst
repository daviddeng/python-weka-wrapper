Examples
========

The following examples are meant to be executed in sequence, as they rely on previous steps,
e.g., on data present.


Start up JVM
------------

.. code-block:: python

   import weka.core.jvm as jvm
   jvm.start()

For more information, check out the help of the `jvm` module:

.. code-block:: python

   help(jvm.start)
   help(jvm.stop)


Location of the datasets
------------------------

The following examples assume the datasets to be present in the `data_dir` directory. For instance,
this could be the following directory:

.. code-block:: python

   data_dir = "/my/datasets/"


Load dataset and print it
-------------------------

.. code-block:: python

   from weka.core.converters import Loader
   loader = Loader(classname="weka.core.converters.ArffLoader")
   data = loader.load_file(data_dir + "iris.arff")
   data.set_class_index(data.num_attributes() - 1)

   print(data)


Build classifier on dataset, print model and draw graph
-------------------------------------------------------

.. code-block:: python

   from weka.classifiers import Classifier
   cls = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.3"])
   cls.build_classifier(data)

   print(cls)

   import weka.plot.graph as graph  # NB: pygraphviz and PIL are required
   graph.plot_dot_graph(cls.graph())


Build classifier incrementally with data and print model
--------------------------------------------------------

.. code-block:: python

   loader = Loader(classname="weka.core.converters.ArffLoader")
   iris_inc = loader.load_file(data_dir + "iris.arff", incremental=True)
   iris_inc.set_class_index(iris_inc.num_attributes() - 1)

   print(iris_inc)

   cls = Classifier(classname="weka.classifiers.bayes.NaiveBayesUpdateable")
   cls.build_classifier(iris_inc)
   for inst in loader:
       cls.update_classifier(inst)

   print(cls)


Cross-validate filtered classifier and print evaluation and display ROC
-----------------------------------------------------------------------

.. code-block:: python

   data = loader.load_file(data_dir + "diabetes.arff")
   data.set_class_index(data.num_attributes() - 1)

   from weka.filters import Filter
   remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "1-3"])

   cls = Classifier(classname="weka.classifiers.bayes.NaiveBayes")

   from weka.classifiers import FilteredClassifier
   fc = FilteredClassifier()
   fc.set_filter(remove)
   fc.set_classifier(cls)

   from weka.classifiers import Evaluation
   from weka.core.classes import Random
   evl = Evaluation(data)
   evl.crossvalidate_model(cls, data, 10, Random(1))

   print(evl.percent_correct())
   print(evl.to_summary())
   print(evl.to_class_details())

   import weka.plot.classifiers as plcls  # NB: matplotlib is required
   plcls.plot_roc(evl, class_index=[0, 1], wait=True)


Cross-validate regressor, display classifier errors and predictions
-------------------------------------------------------------------

.. code-block:: python

   from weka.classifiers import PredictionOutput, KernelClassifier, Kernel
   data = loader.load_file(data_dir + "bolts.arff")
   data.set_class_index(data.num_attributes() - 1)

   cls = KernelClassifier(classname="weka.classifiers.functions.SMOreg", options=["-N", "0"])
   kernel = Kernel(classname="weka.classifiers.functions.supportVector.RBFKernel", options=["-G", "0.1"])
   cls.set_kernel(kernel)
   pout = PredictionOutput(classname="weka.classifiers.evaluation.output.prediction.PlainText")
   evl = Evaluation(data)
   evl.crossvalidate_model(cls, data, 10, Random(1), pout)

   print(evl.to_summary())
   print(pout.get_buffer_content())

   import weka.plot.classifiers as plcls  # NB: matplotlib is required
   plcls.plot_classifier_errors(evl.predictions(), wait=True)


Experiments
-----------

.. code-block:: python

   datasets = [
       data_dir + "iris.arff",
       data_dir + "vote.arff",
       data_dir + "anneal.arff"
   ]
   classifiers = [
       Classifier(classname="weka.classifiers.rules.ZeroR"),
       Classifier(classname="weka.classifiers.trees.J48"),
       Classifier(classname="weka.classifiers.trees.REPTree"),
   ]
   result = "exp.arff"
   from weka.experiments import SimpleCrossValidationExperiment
   exp = SimpleCrossValidationExperiment(
       classification=True,
       runs=10,
       folds=10,
       datasets=datasets,
       classifiers=classifiers,
       result=result)
   exp.setup()
   exp.run()

   loader = weka.core.converters.loader_for_file(result)
   data = loader.load_file(result)
   from weka.experiments import Tester, ResultMatrix
   matrix = ResultMatrix(classname="weka.experiment.ResultMatrixPlainText")
   tester = Tester(classname="weka.experiment.PairedCorrectedTTester")
   tester.set_resultmatrix(matrix)
   comparison_col = data.get_attribute_by_name("Percent_correct").get_index()
   tester.set_instances(data)

   print(tester.header(comparison_col))
   print(tester.multi_resultset_full(0, comparison_col))
   print(tester.multi_resultset_full(1, comparison_col))


Clustering
----------

.. code-block:: python

   data = loader.load_file(data_dir + "vote.arff")
   data.delete_attribute(data.num_attributes() - 1)

   from weka.clusterers import Clusterer
   clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans", options=["-N", "3"])
   clusterer.build_clusterer(data)

   print(clusterer)


Associations
------------

.. code-block:: python

   data = loader.load_file(data_dir + "vote.arff")
   data.set_class_index(data.num_attributes() - 1)

   from weka.associations import Associator
   associator = Associator(classname="weka.associations.Apriori", options=["-N", "9", "-I"])
   associator.build_associations(data)

   print(associator)


Attribute selection
-------------------

.. code-block:: python

   data = loader.load_file(data_dir + "vote.arff")
   data.set_class_index(data.num_attributes() - 1)

   from weka.attribute_selection import ASSearch, ASEvaluation, AttributeSelection
   search = ASSearch(classname="weka.attributeSelection.BestFirst", options=["-D", "1", "-N", "5"])
   evaluator = ASEvaluation(classname="weka.attributeSelection.CfsSubsetEval", options=["-P", "1", "-E", "1"])
   attsel = AttributeSelection()
   attsel.set_search(search)
   attsel.set_evaluator(evaluator)
   attsel.select_attributes(data)

   print("# attributes: " + str(attsel.get_number_attributes_selected()))
   print("attributes: " + str(attsel.get_selected_attributes()))
   print("result string:\n" + attsel.to_results_string())


Data generators
---------------

.. code-block:: python

   from weka.datagenerators import DataGenerator
   generator = DataGenerator(classname="weka.datagenerators.classifiers.classification.Agrawal", options=["-B", "-P", "0.05"])
   DataGenerator.make_data(generator, ["-o", data_dir + "generated.arff"])

   generator = DataGenerator(classname="weka.datagenerators.classifiers.classification.Agrawal", options=["-n", "10", "-r", "agrawal"])
   generator.set_dataset_format(generator.define_data_format())
   print(generator.get_dataset_format())
   if generator.get_single_mode_flag():
       for i in xrange(generator.get_num_examples_act()):
           print(generator.generate_example())
   else:
       print(generator.generate_examples())


Filters
-------

.. code-block:: python

   data = loader.load_file(data_dir + "vote.arff")

   from weka.filters import Filter
   remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "last"])
   remove.set_inputformat(data)
   filtered = remove.filter(data)

   print(filtered)


Packages
--------

.. code-block:: python

   import weka.core.packages as packages
   items = packages.get_all_packages()
   for item in items:
       if item.get_name() == "CLOPE":
           print item.get_name(), item.get_url()

   packages.install_package("CLOPE")
   items = packages.get_installed_packages()
   for item in items:
       print item.get_name(), item.get_url()

   packages.uninstall_package("CLOPE")
   items = packages.get_installed_packages()
   for item in items:
       print item.get_name(), item.get_url()


Stop JVM
--------

.. code-block:: python

   jvm.stop()

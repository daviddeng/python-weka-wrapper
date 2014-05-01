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
   loader = Loader("weka.core.converters.ArffLoader")
   data = loader.load_file(data_dir + "iris.arff")
   data.set_class_index(data.num_attributes() - 1)

   print(data)


Build classifier on dataset, print model and draw graph
-------------------------------------------------------

.. code-block:: python

   from weka.classifiers import Classifier
   cls = Classifier("weka.classifiers.trees.J48")
   cls.set_options(["-C", "0.3"])
   cls.build_classifier(data)

   print(cls)

   import weka.plot.graph as graph
   graph.plot_dot_graph(cls.graph())


Build classifier incrementally with data and print model
--------------------------------------------------------

.. code-block:: python

   loader = Loader("weka.core.converters.ArffLoader")
   iris_inc = loader.load_file(data_dir + "iris.arff", incremental=True)
   iris_inc.set_class_index(iris_inc.num_attributes() - 1)

   print(iris_inc)

   cls = Classifier("weka.classifiers.bayes.NaiveBayesUpdateable")
   cls.build_classifier(iris_inc)
   while True:
       inst = loader.next_instance(iris_inc)
       if inst is None:
           break
       cls.update_classifier(inst)

   print(cls)


Cross-validate filtered classifier and print evaluation and display ROC
-----------------------------------------------------------------------

.. code-block:: python

   data = loader.load_file(data_dir + "anneal.arff")
   data.set_class_index(data.num_attributes() - 1)

   from weka.filters import Filter
   remove = Filter("weka.filters.unsupervised.attribute.Remove")
   remove.set_options(["-R", "1-3"])

   cls = Classifier("weka.classifiers.functions.SMO")

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

   import weka.plot.classifiers as plcls
   plcls.plot_roc(evl, wait=True)


Cross-validate regressor and display classifier errors
------------------------------------------------------

.. code-block:: python

   data = loader.load_file(data_dir + "bolts.arff")
   data.set_class_index(data.num_attributes() - 1)

   cls = Classifier("weka.classifiers.functions.LinearRegression")
   cls.set_options(["-S", "1", "-C"])
   evl = Evaluation(data)
   evl.crossvalidate_model(cls, data, 10, Random(1))

   print(evl.to_summary())

   import weka.plot.classifiers as plcls
   plcls.plot_classifier_errors(evl.predictions(), wait=False)


Experiments
-----------

.. code-block:: python

   datasets = [
       data_dir + "iris.arff",
       data_dir + "vote.arff",
       data_dir + "anneal.arff"
   ]
   classifiers = [
       Classifier("weka.classifiers.rules.ZeroR"),
       Classifier("weka.classifiers.trees.J48"),
       Classifier("weka.classifiers.trees.REPTree"),
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
   matrix = ResultMatrix("weka.experiment.ResultMatrixPlainText")
   tester = Tester("weka.experiment.PairedCorrectedTTester")
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
   clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans")
   clusterer.set_options(["-N", "3"])
   clusterer.build_clusterer(data)

   print(clusterer)


Associations
------------

.. code-block:: python

   data = loader.load_file(data_dir + "vote.arff")
   data.set_class_index(data.num_attributes() - 1)

   from weka.associations import Associator
   associator = Associator("weka.associations.Apriori")
   associator.set_options(["-N", "9", "-I"])
   associator.build_associations(data)

   print(associator)


Attribute selection
-------------------

.. code-block:: python

   data = loader.load_file(data_dir + "vote.arff")
   data.set_class_index(data.num_attributes() - 1)

   from weka.attribute_selection import ASSearch, ASEvaluation, AttributeSelection
   search = ASSearch("weka.attributeSelection.BestFirst")
   search.set_options(["-D", "1", "-N", "5"])
   evaluator = ASEvaluation("weka.attributeSelection.CfsSubsetEval")
   evaluator.set_options(["-P", "1", "-E", "1"])
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
   generator = DataGenerator("weka.datagenerators.classifiers.classification.Agrawal")
   generator.set_options(["-B", "-P", "0.05"])
   DataGenerator.make_data(generator, ["-o", data_dir + "generated.arff"])

   generator = DataGenerator("weka.datagenerators.classifiers.classification.Agrawal")
   generator.set_options(["-n", "10", "-r", "agrawal"])
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
   remove = Filter(classname="weka.filters.unsupervised.attribute.Remove")
   remove.set_options(["-R", "last"])
   remove.set_inputformat(data)
   filtered = remove.filter(data)

   print(filtered)


Stop JVM
--------

.. code-block:: python

   jvm.stop()
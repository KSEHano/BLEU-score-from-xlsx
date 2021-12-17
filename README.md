# BLEU-score-from-xlsx
Collections of functions to calculate the bleu score for translations stored in an xlsx file.

For the use of the programm use the libraries `pandas`, from `nltk.translate` use `bleu_score`, from `openpyxl` use `load_workbook`, `string`, and `random`.

This collection of functions was coded as part of a Bachelor Thesis to prepare and conduct a study on MT quality of different MT systems with BLEU.

read_excel.py contains helpful functions to make references or hypotheses for BLEU from the nltk.translate package as well as slightly changed read and write functions for xlsx using panda read and write functions as well as dataframes. bleu_scores.py uses these functions to calculate the BLEU score for each sentence for each translator as well as a score for each sheet. sen_for_trans.py selects a subset of sentences to use in a study with human translators for example.


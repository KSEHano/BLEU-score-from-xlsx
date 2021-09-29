'''
Author: Kaja Hano
This file contains severa basic functions for the calculation of the bleu score and the writing
an excel file and other functions concerning the bleu score.
'''
import pandas as pd
from openpyxl import load_workbook
import string
from nltk.translate import bleu_score as bleu


def make_ref (df: pd.DataFrame, column : list, is_reference=True):
    '''
    This function takes in a dataframe that contains sentences
    and returns the content in form of a list
    if is_refterence == True equivalent sentences are grouped together
    the returned list is of the form list(list(list(str)))
    else the returned list is of the form list(list(str))
    parameters: 
    :param df: dataframe (rows contain equivalent sentences)
    :param column: list of coulms that will be the used to make the references
    :param is_reference: if a reference shold be made or a hypothesis
    :return: list of sentences
    '''
    #list of all sentences
    sentences = list()
    #list of equivalent sentences
    col_sentences = list()
    #items of the list are words of one sentence
    sentence = list()
    item = ''
    
    for row in df.axes[0]:

        #split each sentence into words
        #for references a extra level of lists is needed       
        if is_reference:
            #this list contains all equivalent sentences
            col_sentences = []
            #split and read for every column
            for col in column:
                #split sentence and put in list
                item = str(df[col][row])
                '''the following steps are included to make the data more comparable and everything that should
                be counted the same is countet as the same and readable for BLEU'''
                item = item.translate(str.maketrans('-', ' '))
                item = item.translate(str.maketrans('', '', string.punctuation))
                item = item.lower()
                #BLEU takes list of words and compares them
                sentence = item.split()
                col_sentences.append(sentence)
            sentences.append(col_sentences)
        #make hypotheses
        #this split is needed because references nees one level more than hypothesis
        else:
            item = str(df[column[0]][row])
            item = item.translate(str.maketrans('', '', string.punctuation))
            item = item.lower()
            sentence = item.split()
            sentences.append(sentence)

    return sentences



def write_excel(file_path, sheet, data):
    '''
    create a new excel file and write into the first sheet
    parameters:
    :param file_path: str. path to file
    :param sheet: str. name of the excel sheet
    :param data: data that is convertable to a DataFrame
    '''
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(file_path)
    df.to_excel(writer, sheet_name = sheet)
    writer.save()
    writer.close()


def add_sheet(file_path: str, sheet: str, data):
    '''
    add data to a new sheet of an existing excel file
    :param file_path: path to target file
    :param sheet: name of the excel sheet
    :param data: data convertable to a pd.Dataframe
    '''
    df = pd.DataFrame(data)
    excel_workbook = load_workbook(file_path)
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    writer.book = excel_workbook
    df.to_excel(writer, sheet_name = sheet)
    writer.save()
    writer.close()


def all_sentence_bleu(name: str, 
    references, 
    hypothesis, 
    weights=(0.25, 0.25, 0.25, 0.25),
    smoothing_function=None,
    auto_reweigh=False):
    '''
    compound all the bleu scores in array per translator
    parameters:
    :param name: for the data collection
    :param refereces: list of references sentences
    :param hyposhesis: list of all hypothesis sentences
    :param weights: weights for bleu score
    :param smothing_function: to smooth the BLEU score
    :param auto_reweight: for bleu score
    :return: a dict of all the scores
    '''
    allscores = []
   
    ref_iter = iter(references)
    #calculate the score for each sentence
    for hypo in hypothesis:
        #put score into array 
        ref = next(ref_iter)
        #calculate the BLEU score for each sentence
        score = bleu.sentence_bleu(ref, hypo, weights, smoothing_function, auto_reweigh)
        allscores.append(score)
    
    return {name: allscores}    


def sheet_corpus_bleu(hypo_names: list, references: list, list_hypothesis: list, 
                    weights = (0.25, 0.25, 0,25, 0.25), smoothing_function=None, auto_reweigh=False):
    '''
    calculates one BLEU score for every set of hypothesis
    parameters:
    :param hypo_name:
    :param refereces: list of references sentences
    :param hyposhesis: list of all hypothesis sentences
    :param weights: weights for bleu score
    :param smothing_function: to smooth the BLEU score
    :param auto_reweight: for bleu score
    :return: a dictionary with all corpus scores with the hypo_name
    '''
    all_corpus={}
    name_iter = iter(hypo_names)
    for hypo in list_hypothesis:
        corpus_score = bleu.corpus_bleu(references, hypo, weights=weights, 
                        smoothing_function=smoothing_function, auto_reweigh= auto_reweigh)
        name = next(name_iter)
        all_corpus[name] = corpus_score

    return all_corpus


def rank_scores(df):
    '''
    calculate rank of all the scores
    Parameters:
    :param df: data that is or is convertibel to a dataframe
    :return: a data frame with all the ranks
    '''
    #ake sure it is a dataframe
    df = pd.DataFrame(df)
    #ranks all rows with the mehod 'min'
    ranks = df.rank(axis=1, method='min', ascending=False)
    return ranks


def average(data_list:list):
    '''
    This function calculates the average of a list of data
    Parameters:
    :param data_list: a list that contains numbers
    :return: the mean ot the list
    '''
    mean = sum(data_list)/len(data_list)
    return mean
 
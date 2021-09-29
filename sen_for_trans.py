'''
Author: Kaja Hano
This function is for the selection of sentences to reduce the dataset of sentences with a bleu score for a
study with humans.
This code is based on using excel files with the translations or scores for each translator in a column. Some keys
and functions are specific to the excel files used in the study.
'''
import pandas as pd
import random
import read_excel as re



def choose_sentences(source_file: str, rank_file: str, result_file:str):
    '''
    takes two files xlsx files with sentences and the bleu results and returns a xlsx file with all the chosen sentences
    the sentences are choosen by length, > 6 words and < 15 to lower bound to have sentences 
    and not only a couple of words, the upper bound to keep evaluating time per sentence reasoable.
    Further, if there are several transaltions that are exactly the same, the whole row is removed
    and at least one bleu score has to be different from the others, so they are more diverse in the mistakes
    from these sentences I randomly draw 50 as a final set of sentences
    parameters:
    :param source_file: file with the collection of sentences, this is written for excel files
    :param rank_file: file with the ranks and bleu scores for the sentences
    :param result_file: files where the choosen sentences will be saved
    '''
    #read the apropriate files
    source = pd.read_excel(source_file, sheet_name = None )
    ranks = pd.read_excel(rank_file, sheet_name = None)
    source_sheets = source.keys()
    #this list will contain the indices for the first reduction
    index_list = []

    #reduce number of sentences further
    # select only sentences with >6 and < 15 words
    for sheet in source_sheets:
        
        for row in source[sheet]['source'].keys():
            sentence = str(source[sheet]['source'][row])
            candidate = sentence.split()

            if len(candidate) > 6 and len(candidate) < 15:
                row_candidate = source[sheet].loc[row]
                #row without douplicates
                no_doubles = row_candidate.drop_duplicates(keep=False)

                #only rows without douplicates will later be considered               
                if len(row_candidate) == len(no_doubles): 
                    index_list.append((sheet, row))
    
    #this list will contain the indices for the sentences after the secons reduction
    index_list2 = []
    ranks_columns = list(ranks['one'].keys())
    try:
        ranks_columns.remove('Unnamed: 0')
    except ValueError:
        ranks_columns = ranks_columns
    
    #iterates over the first list of indices and reduces the number of sentences further
    for i in index_list:
        
        item = ranks[i[0]]['SDL Trados'][i[1]]

        for col in ranks_columns:
            new_item = ranks[i[0]][col][i[1]]

            if item != new_item :
                index_list2.append(i)
                break
                    
    
    #write everything in a file
    index_list_final = random.sample(index_list2, k= 60)
    result = pd.DataFrame()
    
    for i in index_list_final:
        result = result.append(source[i[0]].loc[i[1]], ignore_index=True)
    
    result['indices'] = index_list_final
    #print('from result', result.loc[0])
    re.write_excel(result_file, 'sheet one', result)

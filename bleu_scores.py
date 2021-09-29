'''
Author: Kaja Hano
This file contains a function to calculate the BLEU score of translations in an xlsx file with reference translation
and translations in different columns. With the read_excel file in can be adapted to different 
hyposeses and references as seen in the main.
'''
import pandas as pd
import read_excel as re
from nltk.translate import bleu_score as bleu

def score_translation(source_file: str, target_file: str, reference_list:list, hypotheses_list:list, weights = (0.25, 0.25,0.25,0.25)):
    '''
    This function calculates the BLEU scores for whole excel files
    it includes also ranks and averages of ranks as well ar the corpus bleu score
    Parameters:
    :param source_file: file with the sentences of different translators
    :param target_file: file where the data schould be saved
    :param reference_list: list of columns that are used as references
    :param hypotheses_list: list of hypotheses that are examined
    :param weights: weights used for the BLEU scores
    '''
    
    #make the target file
    df1 = pd.DataFrame()
    #artifact of the programmin in read_excel, leads to an empty sheet
    re.write_excel(target_file,'zero', df1)

    #read the source file
    df = pd.read_excel(source_file, sheet_name=None)
    sheets = df.keys()
    
    #prepare the the averages for all sheets and hypotheses
    df_average = {'Translators': hypotheses_list}
    smoothing = bleu.SmoothingFunction()
    scores = {}
    
    #make all scores for all sheets
    for sheet in sheets:
        
        #collect all the scores for a sheet
        average_rank = []
        average_bleu = []

        for hypo in hypotheses_list:
            new_reference_list = list(reference_list)
            
            #make sure the item is not the hypothesis and in the references
            try:
                new_reference_list.remove(hypo)
            except ValueError:
                new_reference_list = new_reference_list

            #make references and hypotheis for one hypothesis
            references = re.make_ref(df[sheet], new_reference_list)
            hypothesis = re.make_ref(df[sheet], [hypo], is_reference=False)

            #score
            #bleu per sentence
            score = {}
            score = re.all_sentence_bleu(hypo, references, hypothesis, weights=weights, smoothing_function=smoothing.method1)
            scores.update(score)
            #corpus bleu
            corpus_score = bleu.corpus_bleu(references, hypothesis, smoothing_function=smoothing.method1, weights=weights)
            average_bleu.append(corpus_score)
        
        
        #ranks
        #ranks per sentence
        all_ranks = re.rank_scores(scores)
        #put in file
        re.add_sheet(target_file, sheet, scores)
        re.add_sheet(target_file, sheet + ' ranks', all_ranks)

        #rank the things after rank is calculated
        for hypo in hypotheses_list:
            average = re.average(all_ranks[hypo])
            average_rank.append(average)
          
        df_average.update({'Rank : ' + sheet: average_rank,
                    'Bleu: ' + sheet: average_bleu})
    
    #add all averages to the file     
    re.add_sheet(target_file, 'average', df_average)

   

if __name__ == "__main__":
    #these are the bleu default weights, leading to a geometric mean over the n-grams
    #wheights are sorted form uni- to 4-gram
    weight = (0.25, 0.25, 0.25, 0.25)
    #examples for use
    #human reference
    score_translation('path to source file', 'path to target file',
                        ['human'], ['SDL Trados', 'DeepL', 'Bing', 'google'], weights=weight)
    #one against all
    score_translation('path to source file', 'path to target file',
                    ['human', 'SDL Trados', 'DeepL','google', 'Bing'], ['human','SDL Trados', 'DeepL', 'google', 'Bing'], weights=weight)
    
   
    

    
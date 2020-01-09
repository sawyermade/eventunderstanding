#!/usr/bin/python

__author__ = 'fillipe'

import os
import sys
from multiprocessing import Pool


def process_real_data_experiments(args):
    dataset_name = args[0]
    experiments = args[1]
    inference_versions = args[2]
    rank_index = args[3]

    for i in range(len(inference_versions)):
        for j in range(len(experiments)):
            filename = dataset_name + '_' + experiments[j] + '_' + inference_versions[i] + '_performance_summary.txt'
            cmd = 'scp ' + filename + ' 131.247.2.235:~/'
            os.system(cmd)

    cmd = 'ssh 131.247.2.235 "~/summarize_all.py real '+','.join(experiments)+' '+','.join(inference_versions) + \
          ' ' + str(rank_index) + ' ' + dataset_name + '"'
    print cmd
    os.system(cmd)

    image_filename = dataset_name + '_' + '-'.join(experiments) + '_' + '-'.join(inference_versions) + \
                     '_performance-vs-windowsize.png'

    transfer_data = [image_filename]

    for file in transfer_data:
        cmd = 'scp 131.247.2.235:~/'+file+' .'
        os.system(cmd)

    cmd = 'scp -r ' + ' '.join(transfer_data) + " c4lab06.csee.usf.edu:~/public_html/results/real/" + dataset_name + '/'
    os.system(cmd)

def process_experiments(args):
    experiments = args[0]
    inference_versions = args[1]
    degradation = args[2]
    rank = args[3]
    rank_index = args[4]

    for i in range(len(inference_versions)):
        for j in range(len(experiments)):
            filename = experiments[j] + '_' + inference_versions[i] + '_performance_' + \
                                            str(degradation) + 'dl_-1op_' + str(rank) + 'rnk_summary.txt'
            cmd = 'scp ' + filename + ' 131.247.2.235:~/'
            os.system(cmd)

    cmd = 'ssh 131.247.2.235 "~/summarize_all.py synthetic '+','.join(experiments)+' '+','.join(inference_versions)  \
            + ' ' + str(rank_index) + ' ' + str(degradation) + ' ' + str(rank) + '"'
    print cmd
    os.system(cmd)

    image_filename = '-'.join(experiments) + '_' + '-'.join(inference_versions) + '_' + \
                     str(degradation) + 'dl_-1op_' + str(rank) + 'rnk_performance-vs-windowsize.png'

    transfer_data = [image_filename]

    for file in transfer_data:
        cmd = 'scp 131.247.2.235:~/'+file+' .'
        os.system(cmd)

    cmd = 'scp -r ' + ' '.join(transfer_data) + " c4lab06.csee.usf.edu:~/public_html/results/"
    os.system(cmd)

def process_comparison_real_data_results(args):
    dataset_name = args[0]
    experiment_name = args[1]
    inference_versions = args[2]
    ranks = args[3]

    # collect and gather all performance results to be compared
    for i in range(len(inference_versions)):
        filename = dataset_name + '_' + experiment_name + '_' + inference_versions[i] + '_performance_summary.txt'
        cmd = 'scp ' + filename + ' 131.247.2.235:~/'
        os.system(cmd)

    cmd = 'ssh 131.247.2.235 "~/compare_approaches_varying_rank.py real '+experiment_name+' '+','.join(inference_versions) + \
           ' ' + ','.join(ranks) + ' ' + dataset_name + '"'
    print cmd
    os.system(cmd)

    image_filename = dataset_name + '_' + experiment_name + '_' + '-'.join(inference_versions) + '_performance-vs-rank.png'

    transfer_data = [image_filename]

    for file in transfer_data:
        cmd = 'scp 131.247.2.235:~/' + file + ' .'
        os.system(cmd)

    cmd = 'scp -r ' + ' '.join(transfer_data) + " c4lab06.csee.usf.edu:~/public_html/results/real/" + \
          dataset_name + '/' + experiment_name + '/'
    os.system(cmd)

def process_comparison_results(args):
    experiment_name = args[0]
    inference_versions = args[1]
    degradation = args[2]
    rank = args[3]
    ranks = args[4]

    for i in range(len(inference_versions)):
        filename = experiment_name + '_' + inference_versions[i] + '_performance_' + \
                                            str(degradation) + 'dl_-1op_' + str(rank) + 'rnk_summary.txt'
        cmd = 'scp ' + filename + ' 131.247.2.235:~/'
        os.system(cmd)

    cmd = 'ssh 131.247.2.235 "~/compare_approaches_varying_rank.py synthetic ' + experiment_name + ' ' + \
          ','.join(inference_versions) + ' ' + ','.join(ranks) + ' ' + str(degradation) + ' ' + str(rank) + '"'
    print cmd
    os.system(cmd)

    image_filename = experiment_name + '_' + '-'.join(inference_versions) + '_' + \
                     str(degradation) + 'dl_-1op_' + str(rank) + 'rnk_performance-vs-rank.png'

    transfer_data = [image_filename]

    for file in transfer_data:
        cmd = 'scp 131.247.2.235:~/'+file+' .'
        os.system(cmd)

    cmd = 'scp -r ' + ' '.join(transfer_data) + " c4lab06.csee.usf.edu:/home/f/fillipe/public_html/results/" + experiment_name + '/'
    os.system(cmd)


def process_real_data_results(args):
    dataset_name = args[0]
    experiment_name = args[1]
    inference_version = args[2]
    performance_indices = args[3]
    metric = args[4]
    #subpath = args[5] 

    result_name = dataset_name + '_' + experiment_name + '_' + inference_version + '_performance'

    # create
    cmd = 'ssh c4lab06.csee.usf.edu "mkdir -p ~/public_html/results/real/' + dataset_name + '/' + experiment_name + '"'
    print cmd
    os.system(cmd)

    # compute performance summary, including plotting of performance graphs
    cmd = 'scp ' + result_name + '.txt 131.247.2.235:~/'
    print cmd
    os.system(cmd)

    # summarize performance and generate graph plots as images in png format
    cmd = 'ssh 131.247.2.235 "~/cumulative_ranked_performance.py '+result_name+'.txt '+result_name+'_summary.txt '+\
          ' ' + metric + ' ' + ','.join(performance_indices) + '"'
    print cmd
    os.system(cmd)

    # transfer files created in the remote computer to the current computer
    cmd = 'scp 131.247.2.235:~/' + result_name + '*.png .'
    print cmd
    os.system(cmd)
    cmd = 'scp 131.247.2.235:~/' + result_name + '_summary.txt .'
    os.system(cmd)

    # delete images and files in the remote computer
    cmd = 'ssh 131.247.2.235 "rm -r ' + result_name + '*.png"'
    os.system(cmd)
    cmd = 'ssh 131.247.2.235 "rm -r ' + result_name + '*.txt"'
    os.system(cmd)

    # gather files that will be sent to the web repository where the results are kept for display on a web browser
    transfer_data = [result_name+'_summary.txt', result_name+'_summary.png', result_name+'_summary_per_video.png']

    # transfer files containing the summarized results to the web repository
    cmd = 'scp -r ' + ' '.join(transfer_data) + ' c4lab06.csee.usf.edu:~/public_html/results/real/' \
          + dataset_name + '/' + experiment_name + '/'
    os.system(cmd)

    result_name = dataset_name + '_' + experiment_name + '_' + inference_version + '_results'

    # create web page and generate graph images for display
    cmd = './create_results_page.py ' + result_name + ' ' + result_name + '_images ' + result_name
    os.system(cmd)

    transfer_data = [result_name + '_images', result_name + '.html', 'style.css']

    cmd = 'scp -r ' + ' '.join(transfer_data) + ' c4lab06.csee.usf.edu:~/public_html/results/real/' + \
          dataset_name + '/' + experiment_name + '/'
    os.system(cmd)

    cmd = 'rm -r ' + ' '.join(transfer_data)
    os.system(cmd)


def process_results(args):
    experiment_name = args[0]
    inference_version = args[1]
    degradation = args[2]
    rank = args[3]
    performance_indices = args[4]
    metric = args[5]

    #4shots_dynamic_performance_10dl_-1op_2rnk

    folder_name = experiment_name + '_' + inference_version + '_performance' + '_' + str(degradation) + 'dl_-1op_' + str(rank) + 'rnk'

    cmd = 'ssh c4lab06.csee.usf.edu "mkdir ~/public_html/results/'+experiment_name+'"'
    print cmd
    os.system(cmd)

    # compute performance summary, including plotting of performance graphs
    cmd = 'scp '+folder_name+'.txt 131.247.2.235:~/'
    print cmd
    os.system(cmd)

#    cmd = 'ssh 131.247.2.235 \"~/summarize_performance.py '+folder_name+'.txt '+folder_name+'_performance_summary.txt '+\
#          ' ' + ','.join(performance_indices) + '\"'
#    os.system(cmd)

    cmd = 'ssh 131.247.2.235 "~/cumulative_ranked_performance.py '+folder_name+'.txt '+folder_name+'_summary.txt '+\
          ' ' + metric + ' ' + ','.join(performance_indices) + '"'
    print cmd
    os.system(cmd)

    cmd = 'scp 131.247.2.235:~/'+folder_name+'*.png .'
    print cmd
    os.system(cmd)

    cmd = 'scp 131.247.2.235:~/'+folder_name+'_summary.txt .'
    os.system(cmd)

    cmd = 'ssh 131.247.2.235 "rm -r '+folder_name+'*.png"'
    os.system(cmd)

    cmd = 'ssh 131.247.2.235 "rm -r '+folder_name+'*.txt"'
    os.system(cmd)

    transfer_data = [folder_name+'_summary.txt', folder_name+'_summary.png', folder_name+'_summary_per_video.png']

    cmd = 'scp -r ' + ' '.join(transfer_data) + " c4lab06.csee.usf.edu:/home/f/fillipe/public_html/results/" + experiment_name + '/'
    os.system(cmd)

    folder_name = experiment_name + '_' + inference_version + '_results_' + str(degradation) + 'dl_-1op_' + str(rank) + 'rnk'

    # create web page and generate graph images for display
    cmd = './create_results_page.py ' + folder_name + ' ' + folder_name + '_images ' + folder_name
    os.system(cmd)

    transfer_data = [folder_name + '_images', folder_name + '.html', 'style.css']

    cmd = 'scp -r ' + ' '.join(transfer_data) + " c4lab06.csee.usf.edu:/home/f/fillipe/public_html/results/" + experiment_name + '/'
    os.system(cmd)

    cmd = 'rm -r ' + ' '.join(transfer_data)
    os.system(cmd)

def main():

    if len(sys.argv) < 3:
        print 'usage: ./organize_results.py real|synthetic experiment_name [task=all|results|comparison] [dataset_name]'
        print 'or usage: ./organize_results.py real|synthetic experiments task=experiment rank_index=10 dataset_name'
        exit(1)

    number_of_processes = 8
    pool = Pool(number_of_processes)

    experiment_type = sys.argv[1]
    experiment_name = sys.argv[2]
    print experiment_name

    if len(sys.argv) > 2:
        task_type = sys.argv[3]
    else:
        task_type = 'all'

    if task_type == 'experiment':
        rank_index = int(sys.argv[4])
        if experiment_type == 'real':
            dataset_name = sys.argv[5]
    else:
        if experiment_type == 'real':
            dataset_name = sys.argv[4]

#    output_filename = sys.argv[2]

#    name = input_filename.split('/')[-1].split('.')[-2]
    performance_indices = ['1','3','5']
    ranks = map(str,range(1,11))

    metric = 'generator_set'
    rank_range = [2, 3, 1]
    degradation_range = [10, 70, 10]
    #inference_version = ['dynamic', 'notemporalbonds', 'temporalbonds']
    inference_version = ['notemporalbonds', 'temporalbonds']

    # assemble tasks
    if task_type == 'all' or task_type == 'results':
        tasks = []
        for version in inference_version:
            print version
            if experiment_type == 'synthetic':
                for d in range(degradation_range[0], degradation_range[1], degradation_range[2]):
                    print d
                    for r in range(rank_range[0],rank_range[1],rank_range[2]):
                        print r
                        #tasks.append((experiment_name, version, d, r, performance_indices))
                        tasks.append((experiment_name, version, d, r, ranks, metric))
                        print repr(tasks[-1])

            else:
                tasks.append((dataset_name, experiment_name, version, ranks, metric))
                print repr(tasks[-1])

        if experiment_type == 'synthetic':
            pool.map(process_results, tasks)
        else:
            pool.map(process_real_data_results, tasks)

    # assemble tasks for processing comparison results
    if task_type == 'all' or task_type == 'comparison':
        tasks = []
        if experiment_type == 'synthetic':
            for d in range(degradation_range[0], degradation_range[1], degradation_range[2]):
                print d
                for r in range(rank_range[0],rank_range[1],rank_range[2]):
                    print r
                    tasks.append((experiment_name, inference_version, d, r, ranks))
                    print repr(tasks[-1])
        else:
            tasks.append((dataset_name, experiment_name, inference_version, ranks))
            print repr(tasks[-1])

        if experiment_type == 'synthetic':
            pool.map(process_comparison_results, tasks)
        else:
            pool.map(process_comparison_real_data_results, tasks)

    # assemble tasks for processing comparison results
    if task_type == 'experiment':
        tasks = []
        if experiment_type == 'synthetic':
            for d in range(degradation_range[0], degradation_range[1], degradation_range[2]):
                print d
                for r in range(rank_range[0],rank_range[1],rank_range[2]):
                    print r
                    tasks.append((experiment_name.split(','), inference_version, d, r, rank_index))
                    print repr(tasks[-1])
        else:
            tasks.append((dataset_name, experiment_name.split(','), inference_version, rank_index))
            print repr(tasks[-1])

        if experiment_type == 'synthetic':
            pool.map(process_experiments, tasks)
        else:
            pool.map(process_real_data_experiments, tasks)

if __name__ == '__main__':
    main()
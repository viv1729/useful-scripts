import pickle

dictionary = {"user" : "vivek.a",
                "backup_dir" : f"/home/vivek.a/research-backup/",
                "root_dir" : f"/home/vivek.a/",

                "skip_dirs" : [ ".git", 
                               ".ipynb_checkpoints", 
                               ".data", 
                               "__pycache__",

                                f"/home/vivek.a/isb/data_business",
                                f"/home/vivek.a/isb/data_sample",
                                f"/home/vivek.a/isb/data_sp_russell",
                                f"/home/vivek.a/isb/data_sp_russell2",  
                                f"/home/vivek.a/isb/data_yearly",


                                f"/home/vivek.a/isb/10k_scrape/data_old-full",
                                f"/home/vivek.a/isb/10k_scrape/data_sp-100",

                                f"/home/vivek.a/isb/summary/data_cnn_dm",
                                f"/home/vivek.a/isb/summary/op_10K-s&p500",
                                f"/home/vivek.a/isb/summary/op_bertSum",
                                f"/home/vivek.a/isb/summary/data_newsroom",

                                f"/home/vivek.a/isb/summary/doc2tweet/op_final_tweets_json",
                                f"/home/vivek.a/isb/summary/doc2tweet/data_news",

                                f"/home/vivek.a/kp_extraction/data_paper_abstracts/kp20k/base/keyphrase",
                                f"/home/vivek.a/kp_extraction/data_paper_abstracts/kp20k/base/text_processed",
                                f"/home/vivek.a/kp_extraction/data_paper_abstracts/kp20k/base/text",

                                f"/home/vivek.a/kp_extraction/baselines/data/gold_meta-qw",
                                f"/home/vivek.a/kp_extraction/baselines/data/input_processed",
                                f"/home/vivek.a/kp_extraction/baselines/data/input",
                                f"/home/vivek.a/kp_extraction/baselines/data/raw",

                                f"/home/vivek.a/kp_extraction/baselines/op_EmbedRank",
                                f"/home/vivek.a/kp_extraction/baselines/op_TextRank",

                                f"/home/vivek.a/tech_companies",

                                f"/home/vivek.a/Embeddings/CoreNLP-full-2018-02-27",
                            ],

                "large_dirs" : ["isb", "kp_extraction", "others"],

                "folders_to_backup" : ['git_repos',
                                     'courses',
                                     'HASOC-2019',
                                     'datasets',
                                     'Domain-Indentification',
                                     'kp_extraction',
                                     'isb',
                                     'temp',
                                     'nltk_data',
                                     'ML',
                                     'college',
                                     'Embeddings',
                                     'others']

                }



with open("backup_config.pkl", "wb") as op:
	pickle.dump(dictionary, op)

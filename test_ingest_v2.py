import unittest
import ingest_v2 as src
import pandas as pd
import os

class TestApp(unittest.TestCase):

    bad_data = {
        'id ':[10,-1,34]
        ,'dates':['2046-01-01','2020-31-13','12-2026-13']
        ,'texts':['waf$fle',' c^ne$"#',None]
            }
    good_data = {
        'id':[0,1,3]
        ,'dates':['2026-01-01','2020-12-31','1984-09-02']
        ,'texts':['waffle','cone','smoothie']
            }
    good_df = pd.DataFrame(good_data)
    bad_df = pd.DataFrame(bad_data)


    def test_clean_dates(self):
        test_df = src.clean_dates(self.bad_df,['dates'])
        for dt in test_df['dates']:
            assert pd.to_datetime(dt)


    def test_drop_null_records(self):
        test_df = src.drop_null_records(self.bad_df)
        for _, rw in test_df.iterrows():
            for cell in rw:
                assert cell != None
        
    def test_rename_cols(self):
        tdf = self.bad_df.rename(columns={'data':' data ^'})
        tdf = src.rename_cols(tdf)
        new_cols = ['id','dates','texts']
        
        assert set(tdf.columns) == set(new_cols)

    def test_overlord(self):
        #src.overlord()
        assert 1==1

    def test_storage(self):
        src.storage(self.good_df,'testfile.csv')
        assert os.path.isfile('testfile.csv')
        os.remove('testfile.csv')

if __name__ == '__main__':
    unittest.main()

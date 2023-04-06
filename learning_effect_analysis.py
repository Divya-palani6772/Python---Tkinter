import pandas as pd
from statsmodels.stats.anova import AnovaRM
import pingouin as pg
import researchpy

pd.set_option('display.max_columns', None)
df = pd.read_excel('Data.xlsx')
pd_summary = researchpy.summary_cont(df.groupby(['ThumbType', 'Block'])['TaskTime']).round(2).reset_index()
print(pd_summary)

df_rt = df[df['ThumbType'] == 'right']  # get the dataframe of right thumb
res_rt = AnovaRM(data=df_rt, depvar='TaskTime', subject='Participant', within=['Block'], aggregate_func='mean')

print(res_rt.fit())

post_hocs_rt = pg.pairwise_tests(dv='TaskTime', within='Block', subject='Participant', padjust='bonf', data=df_rt)

print(post_hocs_rt)

#task -> do for left thumb
# result
# F(2,6) = 1.55 , p = 0.26, Blocks didnot have impact on task time because p > 0.05. The mean time for blocks 1, 2, 3 was 2627, 2456, 2508 ms respectively.
# pairwise comparisons revealed no significant differences between each two blocks (p > 0.23) NOTE: if when p < 0.05 then there is significant differences
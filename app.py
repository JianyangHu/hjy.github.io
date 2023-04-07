import streamlit as st

import pandas as pd
from PIL import Image
from visualization.passing_network import draw_pitch, draw_pass_map
import matplotlib.pyplot as plt
# 引入 FigureCanvasAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg
# 引入 Image
import numpy as np
import PIL.Image as Image

data_all=pd.read_csv("中超2021_pass.csv")


def gendata(matchid,teamid):
    data=pd.read_csv("中超2021_pass.csv")
    data=data[(data["MATCH_ID"]==matchid) & (data["FROM_TEAM_ID"]==teamid)& (data["TO_TEAM_ID"]==teamid)][:]


    data=data[["FROM_PERSON_NAME","FROM_PERSON_X","FROM_PERSON_Y","TO_PERSON_NAME","TO_PERSON_X","TO_PERSON_Y"]]
    data=data.dropna()

    return data
    


def plot_passing_netowrk(passing_data):
    passing_data=passing_data
   
    data=passing_data[["FROM_PERSON_NAME","FROM_PERSON_X","FROM_PERSON_Y","TO_PERSON_NAME"]]
    data=data.dropna()
    s1=passing_data[["FROM_PERSON_NAME","FROM_PERSON_X","FROM_PERSON_Y"]]
    s2=passing_data[["TO_PERSON_NAME","TO_PERSON_X","TO_PERSON_Y"]]
    s2.columns=["FROM_PERSON_NAME","FROM_PERSON_X","FROM_PERSON_Y"]

    s=pd.concat((s1,s2),axis=0)
    player_position=s

   
    #######position
    player_position=player_position.groupby("FROM_PERSON_NAME").mean()

    player_position.index.name="player_name"

    player_position.columns=["origin_pos_x","origin_pos_y"]
    player_position["origin_pos_x"]=player_position["origin_pos_x"]/620
    player_position["origin_pos_y"]=1-(player_position["origin_pos_y"])/420
    
    
    
    #########pass count
    player_pass_count=s.copy()
    player_pass_count=pd.DataFrame(player_pass_count.groupby("FROM_PERSON_NAME").count().iloc[:,1])
    player_pass_count.index.name="player_name"
    player_pass_count.columns=["num_passes"]
    player_pass_count


    player_pass_value=player_pass_count.copy()
    player_pass_value.columns=["pass_value"]

    set_name={}
    #############pair count
    pair_pass_count=data.copy()
    pair_pass_count=pair_pass_count.reset_index()
    

    for i in range(len(pair_pass_count)):
        set_name[str(pair_pass_count.loc[i,"FROM_PERSON_NAME"])+"_"+str(pair_pass_count.loc[i,"TO_PERSON_NAME"])]=0

    for i in range(len(pair_pass_count)):
        set_name[str(pair_pass_count.loc[i,"FROM_PERSON_NAME"])+"_"+str(pair_pass_count.loc[i,"TO_PERSON_NAME"])]+=1

    pair_pass_count=pd.DataFrame(set_name,index=["num_passes"]).T

    pair_pass_count.index.name="pair_key"

    pair_pass_value=pair_pass_count.copy()

    pair_pass_value.columns=["pass_value"]


    from visualization.passing_network import draw_pitch, draw_pass_map
    import matplotlib.pyplot as plt
    plt.rcParams["font.sans-serif"]=["Songti SC"] #设置字体
    plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
    plot_title =""

    plot_legend = "Location: pass origin\nSize: number of passes\nColor: number of passes"


    ax = draw_pitch()
    ax = draw_pass_map(ax, player_position, player_pass_count, player_pass_value,
                pair_pass_count, pair_pass_value, plot_title, plot_legend)

    canvas = FigureCanvasAgg(plt.gcf())

    # 绘制图像
    canvas.draw()
    # 获取图像尺寸
    w, h = canvas.get_width_height()
    # 解码string 得到argb图像
    buf = np.fromstring(canvas.tostring_argb(), dtype=np.uint8)



    # 重构成w h 4(argb)图像
    buf.shape = (w, h, 4)
    # 转换为 RGBA
    buf = np.roll(buf, 3, axis=2)
    # 得到 Image RGBA图像对象 (需要Image对象的同学到此为止就可以了)
    image = Image.frombytes("RGBA", (w, h), buf.tostring())


    return image






option_match = st.selectbox(
    'Which match？',
    set(data_all["MATCH_ID"].unique()))



option_team=st.selectbox(
"Which team?",
set(data_all[data_all["MATCH_ID"]==option_match]["FROM_TEAM_ID"].unique())

)


if st.button('Start'):
    image=plot_passing_netowrk(gendata(option_match,option_team))



    st.image(image, caption='passing network ')

    st.write('Finished')
else:
    st.write('Click here to generate the passing network')



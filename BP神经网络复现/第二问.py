import math,random
import numpy as np

def sigmoid(x,deriv=False):
    if(deriv):
        return x(1-x)
    else:
        return 1 / (1 + math.exp(-x))

x=[[i//8, (i&4)>>2,(i&2)>>1 ,i%2]for i in range(16)]  ##训练集
res=[(sum(x[i])+1)%2 for i in range(16)]   ##结果
idx = [i for i in range(16)]
alpha=0.9

##开始对yita从0.05~0.5遍历
for k in range(9,10):
    v = [[random.uniform(-1, 1) for i in range(4)] for j in range(4)]
    w = [random.uniform(-1, 1) for i in range(4)]
    bias = [random.uniform(-1, 1) for i in range(5)]  ##b0表示下一层的偏移，b1~b4为第一层偏移
    s = [random.uniform(-1, 1) for i in range(4)]
    yita=0.05+0.05*k
    epoch=1
    last_bgrad,last_wgrad,last_vgrad=np.array([0] * 5), np.array([0] * 4), np.array([[0 for i in range(4)] for j in range(4)])
    while(True):

        ##每一批抽14个来训练
        idx_temp=np.random.choice(idx,14,replace=False)
        x_temp,res_temp=[],[]
        for i in idx_temp:
            x_temp.append(x[i])
            res_temp.append(res[i])

        b_grad, w_grad, v_grad = np.array([0.0] * 5), np.array([0.0] * 4), np.array([[0.0 for i in range(4)] for j in range(4)])  ##容纳每一批的梯度变化总和
        for t in range(14):
            tb_grad, tw_grad, tv_grad = np.array([0.0] * 5), np.array([0.0] * 4), np.array([[0.0 for i in range(4)] for j in range(4)])  ##某一对x,y对应的各种临时梯度
            for j in range(4):
                s_temp=bias[j+1]
                for i in range(4):
                    s_temp+=x_temp[t][i]*v[i][j]
                s[j]=sigmoid(s_temp)
            y_temp=bias[0]
            for i in range(4):
                y_temp+=w[i]*s[i]
            y=sigmoid(y_temp)
            if epoch%1000==0:
                print('epoch=',epoch,'y=',y,' ',res[t])

            ##更新梯度
            y_loss=y-res_temp[t]
            tb_grad[0]=y_loss*y*(1-y)
            b_grad[0]+=tb_grad[0]
            for i in range(4):
                tw_grad[i]=tb_grad[0]*s[i]
                tb_grad[i+1]=tb_grad[0]*w[i]*s[i]*(1-s[i])
                w_grad[i]+=tw_grad[i]
                b_grad[i+1]+=tb_grad[i+1]
            for j in range(4):
                for i in range(4):
                    tv_grad[i][j]=tb_grad[j+1]*x_temp[t][i]
                    v_grad[i][j]+=tv_grad[i][j]
        ##更新参数
        if epoch==1:
            last_bgrad=b_grad
            last_vgrad=v_grad
            last_wgrad=w_grad
        else:
            last_bgrad=last_bgrad*alpha+b_grad
            last_vgrad=last_vgrad*alpha+v_grad
            last_wgrad=last_wgrad*alpha+w_grad

        for i in range(5):
            bias[i]-=yita*last_bgrad[i]
        for i in range(4):
            w[i]-=yita*last_wgrad[i]
        for j in range(4):
            for i in range(4):
                v[i][j] -= yita * last_vgrad[i][j]

        ##判断是否可以终止
        flag=True
        for t in range(16):
            for j in range(4):
                s_temp=bias[j+1]
                for i in range(4):
                    s_temp+=x[t][i]*v[i][j]
                s[j]=sigmoid(s_temp)
            y_temp=bias[0]
            for i in range(4):
                y_temp+=w[i]*s[i]
            y=sigmoid(y_temp)
            if abs(res[t]-y)>0.05:
                flag=False
                epoch+=1
                break
        if flag:
            #print('Net stop at {} turn'.format(epoch))
            break
    print("yita={} ,net stop at epoch {}".format(yita,epoch))



## ML ToolKit安装和使用指南

[TOC]

### 框架比较

| **库名称**    | **开发语言**                                 | **速度** | **灵活性** | **文档** | **适合模型**  | **平台**                                   | **上手难易** |
| ---------- | ---------------------------------------- | ------ | ------- | ------ | --------- | ---------------------------------------- | -------- |
| Caffe      | c++/cuda                                 | 快      | 一般      | 全面     | CNN       | 所有系统                                     | 中等       |
| TensorFlow | c++/cuda/[Python](http://lib.csdn.net/base/python) | 中等     | 好       | 中等     | CNN/RNN   | [Linux](http://lib.csdn.net/base/linux), OSX | 难        |
| MXNet      | c++/cuda                                 | 快      | 好       | 全面     | CNN       | 所有系统                                     | 中等       |
| `Torch`    | `c/lua/cuda`                             | `快`    | `好`     | `全面`   | `CNN/RNN` | `Linux, OSX`                             | `中等`     |
| Theano     | python/c++/cuda                          | 中等     | 好       | 中等     | CNN/RNN   | Linux, OSX                               | 易        |

### tensorflow

Google开源的其第二代深度学习技术——被使用在Google搜索、图像识别以及邮箱的深度学习框架。

是一个理想的RNN（递归神经网络）API和实现，TensorFlow使用了向量运算的符号图方法，使得新网络的指定变得相当容易，支持快速开发。缺点是速度慢，内存占用较大。（比如相对于Torch）

> 编程系统，支持C++和Python

#### 安装

> **安装gcc g++**
> yum install gcc  
> yum install gcc-c++ 
>
> **安装numpy scipy**
> yum install numpy
> yum install scipy
>
> **安装ez_setup**
> wget http://peak.telecommunity.com/dist/ez_setup.py
> python ez_setup.py
>
> **安装pip**
> wget --no-check-certificate https://github.com/pypa/pip/archive/1.5.5.tar.gz
> tar zvxf 1.5.5.tar.gz    #解压文件
> cd pip-1.5.5/
> python setup.py install
> 或者
> wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
> python get-pip.py
>
>
> **pip安装tensorflow**
> sudo pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0rc0-cp27-none-linux_x86_64.whl
>
> **安装后目录**
> /usr/lib/python2.7/site-packages/tensorflow/

#### 使用

##### 基本概念

- 使用graph表示计算任务
- 在被称之为会话（session）的上下文(context)中执行图
- 使用tensor表示数据
- 通过变量（variable）维护状态（也即权值）
- 使用feed和fetch可以为任意的操作赋值或者从其中获取数据



#### 参考

[极客学院tensorflow教程](http://wiki.jikexueyuan.com/project/tensorflow-zh/get_started/basic_usage.html)

---

### mxnet

mxnet直接编译安装在`/usr/local/mexnet`目录下，其中配置和安装文件等都在这个目录下，在software目录不再保留其源码文件

#### 安装

##### python

```
pip install mxnet
```

#### 使用

##### python

```python
>>> import mxnet as mx
>>> a = mx.nd.ones((2, 3))
>>> b = a * 2 + 1
>>> b.asnumpy()
array([[ 3.,  3.,  3.],
       [ 3.,  3.,  3.]], dtype=float32)
```

#### 参考

[MxNet官方安装指南](http://mxnet.io/get_started/install.html)

[MxNet官方教程](http://mxnet.io/tutorials/index.html)

---

### Torch

Torch是Facebook力推的深度学习框架，主要是C和Lua开发，有较好的灵活性和速度。

> torch是用lua编写，支持动态计算图（这点和tensorflow不一样，tensorflow支持的是静态计算图），pytorch是torch的python接口，是的在python中调用torch进行机器学习变得方便，不需要再打包接口

#### 安装Torch

##### 平台指导

**Self-contained Torch installation**:Please refer to the [Torch installation guide](http://torch.ch/docs/getting-started.html#_) for details on how to make a fresh install of Torch on Linux or MacOS.

If on windows with msvc, please refer to this [guide](win-files/README.md) for details on installation and usage.

##### 安装过程说明

###### **Install**

- Dependencies

Globally installed dependencies can be installed via:

```bash
bash install-deps

#在这一步中会安装很多的依赖项，如openblas，gnuplot等
```

- Lua and Torch

The self-contained Lua and Torch installations are performed via:

```bash
./install.sh

#在这一步中会安装luajit,luasocks及torch的nn,ipath等核心功能包（不要忘记torch是用lua）
```

By default Torch will install LuaJIT 2.1. If you want other options, you can use the command:

```bash
# If a different version was installed, used ./clean.sh to clean it
TORCH_LUA_VERSION=LUA51 ./install.sh
TORCH_LUA_VERSION=LUA52 ./install.sh
```

###### Update

To update your already installed distro to the latest `master` branch of `torch/distro` simply run:

```bash
./update.sh
```

###### Cleaning

To remove all the temporary compilation files you can run:

```bash
./clean.sh
```

To remove the installation run:

```bash
# Warning: this will remove your current installation
rm -rf ./install
```

You may also want to remove the `torch-activate` entry from your shell start-up script (`~/.bashrc` or `~/.profile`).

###### Test

You can test that all libraries are installed properly by running:

```bash
./test.sh
```

Tested on Ubuntu 14.04, CentOS/RHEL 6.3 and OSX

#### 安装PyTorch

pytorch是torch的python接口实现，不依赖原有的torch，可以单独使用

```shell
git clone https://github.com/hughperkins/pytorch.git
cd pytorch/
pip install -r requirements.txt
pip install -r test/requirements.txt
source ~/torch/install/bin/torch-activate

# 在build之前，先将~/torch/install/bin/目录添加到PATH环境变量中去，不然提示报错找不到Luajit
./build.sh
```

当提示以下内容则代表安装成功：

> Finished processing dependencies for PyTorch===4.1.1-SNAPSHOT

If you also see this output at the bottom of your terminal, congraulations! You have successfully installed PyTorch!

####  使用

//待完善

#### 参考

[Pytorch深度学习:60分钟快速入门](https://zhuanlan.zhihu.com/p/25572330)

[pytorch:Torch的python支持](http://www.toutiao.com/a6377633223488733441/)

[Torch官方安装指南](http://torch.ch/docs/getting-started.html#_)

[Tutorial: Deep Learning in PyTorch](https://iamtrask.github.io/2017/01/15/pytorch-tutorial/?utm_source=tuicool&utm_medium=referral)（近乎官方入门指南:推荐）

[PyTorch参考手册](http://pytorch.org/tutorials/)

[Github的Pytorch的例子](https://github.com/pytorch/examples)






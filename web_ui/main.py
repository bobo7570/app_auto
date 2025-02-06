import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import pytest  # type: ignore

# 添加项目根目录到Python路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from utils.driver import AppiumDriver
from utils.device_manager import DeviceManager
from config import load_config

class AutoTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("移动端自动化测试平台")
        self.root.geometry("1000x700")
        
        # 设置主题样式
        style = ttk.Style()
        style.theme_use('clam')  # 使用clam主题
        
        # 配置样式
        style.configure('TFrame', background='#f0f4f7')  # 添加背景色
        style.configure('Title.TLabel', font=('微软雅黑', 18, 'bold'), foreground='#2c3e50', background='#f0f4f7')
        style.configure('Header.TLabel', font=('微软雅黑', 11), foreground='#34495e', background='#f0f4f7')
        style.configure('TButton', font=('微软雅黑', 10), borderwidth=1)
        style.configure('Run.TButton', font=('微软雅黑', 12), 
                        foreground='white', background='#3498db',
                        padding=12, borderwidth=2, 
                        relief='raised', width=15)
        style.map('Run.TButton', 
                 background=[('active', '#2980b9'), ('disabled', '#bdc3c7')],
                 relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="25")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.config(relief='flat', style='TFrame')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(self.main_frame, text="移动端自动化测试平台", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 添加装饰性元素
        deco_frame = ttk.Frame(self.main_frame, height=4, style='TFrame')
        deco_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 15))
        ttk.Separator(self.main_frame, orient='horizontal').grid(row=0, column=0, columnspan=3, 
                                                               sticky='ew', pady=(0, 15))
        
        # 调整布局比例
        self.main_frame.columnconfigure(0, weight=1, uniform='group1')
        self.main_frame.columnconfigure(1, weight=3, uniform='group1')
        
        # 创建左侧和右侧框架
        left_frame = ttk.LabelFrame(self.main_frame, text="配置区域", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        right_frame = ttk.LabelFrame(self.main_frame, text="测试用例", padding="10")
        right_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 左侧配置区域
        # 平台选择
        ttk.Label(left_frame, text="测试平台:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=10)
        self.platform_var = tk.StringVar(value="iOS")
        platform_combo = ttk.Combobox(left_frame, textvariable=self.platform_var, width=30, state='readonly', font=('微软雅黑', 10))
        platform_combo['values'] = ("iOS", "Android")
        platform_combo.grid(row=0, column=1, sticky=tk.W, pady=10, padx=5)
        platform_combo.bind('<<ComboboxSelected>>', self.update_devices)
        
        # 设备选择
        ttk.Label(left_frame, text="测试设备:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=10)
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(left_frame, textvariable=self.device_var, 
                                       width=28, state='readonly',
                                       font=('微软雅黑', 10))
        self.device_combo.grid(row=1, column=1, sticky=tk.W, pady=10, padx=5)
        
        # 刷新设备按钮
        refresh_btn = ttk.Button(left_frame, text="🔄 刷新设备", command=self.update_devices)
        refresh_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # 右侧测试用例区域
        # 测试用例列表框
        self.test_frame = ttk.Frame(right_frame)
        self.test_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # 创建测试用例树形视图
        self.test_tree = ttk.Treeview(self.test_frame, selectmode='extended', 
                                    show='tree', style='Custom.Treeview')
        self.test_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        tree_scroll = ttk.Scrollbar(self.test_frame, orient=tk.VERTICAL, command=self.test_tree.yview)
        tree_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.test_tree.configure(yscrollcommand=tree_scroll.set)
        
        # 底部按钮区域
        bottom_frame = ttk.Frame(self.main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        # 执行按钮
        self.run_button = ttk.Button(
            bottom_frame, 
            text="▶ 开始测试", 
            command=self.run_tests,
            style='Run.TButton',
            width=20
        )
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        # 查看报告按钮
        self.report_button = ttk.Button(
            bottom_frame,
            text="📊 查看报告",
            command=self.open_report,
            style='Run.TButton',
            width=20
        )
        self.report_button.pack(side=tk.LEFT, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                              relief=tk.FLAT, anchor=tk.W,
                              font=('微软雅黑', 9), foreground='#7f8c8d',
                              background='#ecf0f1')
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # 添加执行进度条（在状态栏上方）
        self.progress = ttk.Progressbar(self.main_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky='ew', pady=(5,0))
        
        # 初始化数据
        self.load_test_cases()
        self.update_devices()
        
    def load_test_cases(self):
        """加载测试用例到树形视图"""
        self.test_tree.delete(*self.test_tree.get_children())
        test_cases = discover_tests()
        
        # 按目录组织测试用例
        test_dirs = {}
        for case in test_cases:
            dir_name = os.path.dirname(case)
            if dir_name not in test_dirs:
                test_dirs[dir_name] = []
            test_dirs[dir_name].append(os.path.basename(case))
        
        # 在树形视图中添加图标支持
        self.tree_icon_folder = tk.PhotoImage(file='assets/folder.png').subsample(20,20)
        self.tree_icon_file = tk.PhotoImage(file='assets/file.png').subsample(20,20)
        
        # 添加到树形视图
        for dir_name, cases in test_dirs.items():
            dir_item = self.test_tree.insert('', 'end', text=dir_name, 
                                           image=self.tree_icon_folder, 
                                           open=True)
            for case in cases:
                self.test_tree.insert(dir_item, 'end', text=case, 
                                    image=self.tree_icon_file,
                                    values=(os.path.join(dir_name, case),))
            
    def update_devices(self, event=None):
        """更新设备列表"""
        self.status_var.set("正在刷新设备列表...")
        platform = self.platform_var.get()
        devices = get_devices(platform)
        self.device_combo['values'] = devices
        if devices:
            self.device_combo.set(devices[0])
        self.status_var.set("设备列表已更新")
            
    def run_tests(self):
        """执行测试用例"""
        selected_items = self.test_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请选择至少一个测试用例")
            return
            
        # 获取选中的测试用例完整路径
        selected_tests = []
        for item in selected_items:
            if self.test_tree.parent(item):  # 如果是叶子节点（测试用例）
                selected_tests.append(self.test_tree.item(item)['values'][0])
        
        if not selected_tests:
            messagebox.showwarning("警告", "请选择具体的测试用例文件")
            return
            
        platform = self.platform_var.get()
        device = self.device_var.get()
        
        try:
            # 更新状态
            self.status_var.set("测试执行中...")
            self.run_button['state'] = 'disabled'
            self.root.update()
            
            # 执行测试
            config = load_config()
            config['devices'][platform.lower()]['udid'] = device
            
            driver = AppiumDriver.get_driver(
                platform=platform.lower(),
                config=config
            )
            
            pytest_args = [
                "-v",
                f"--alluredir=./report/allure_{platform.lower()}",
                f"--device={device}",
                f"--platform={platform.lower()}"
            ]
            pytest_args.extend(selected_tests)
            
            # 在测试执行过程中更新进度
            def update_progress(current, total):
                self.progress['value'] = (current/total)*100
                self.root.update()
            
            # 修改pytest执行部分（示例）
            total_cases = len(selected_tests)
            for i, case in enumerate(selected_tests):
                # 执行单个测试用例
                pytest.main([case] + pytest_args)
                update_progress(i+1, total_cases)
            
            messagebox.showinfo("成功", "测试执行完成！")
            self.status_var.set("测试执行成功")
        except Exception as e:
            messagebox.showerror("错误", f"执行异常：{str(e)}")
            self.status_var.set("测试执行出错")
        finally:
            self.run_button['state'] = 'normal'
            AppiumDriver.quit_driver()
            
    def open_report(self):
        """打开测试报告"""
        platform = self.platform_var.get()
        report_path = f"./report/allure_{platform.lower()}/index.html"
        if os.path.exists(report_path):
            os.system(f"start {report_path}")
        else:
            messagebox.showinfo("提示", "暂无测试报告")

def discover_tests() -> list:
    """发现可用的测试用例"""
    test_dir = "test_cases"
    test_cases = []
    
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_path = os.path.join(root, file)
                test_cases.append(test_path)
    
    return test_cases

def get_devices(platform: str) -> list:
    """获取可用设备列表"""
    if platform == "iOS":
        return DeviceManager().get_ios_devices()
    return ["模拟器", "真机"]  # Android设备发现需扩展

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTestGUI(root)
    root.mainloop() 
# 简单的批量下载脚本，单线程执行模式，结束后有暂停可查看日志。
# 获取当前目录下所有的 Python 文件
$pythonFiles = Get-ChildItem -Path . -Filter *.py | Sort-Object Name

# 按顺序运行每个 Python 文件
foreach ($file in $pythonFiles) {
    Write-Host "正在运行: $($file.FullName)"
    python $file.FullName
}

# 所有任务执行完后暂停
Read-Host -Prompt "所有任务执行完毕，按 Enter 键退出"
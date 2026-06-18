@echo off
echo ===== 后端启动指南 =====
echo.
echo 步骤1：确保 Docker Desktop 在运行（任务栏有 Docker 图标）
echo.
echo 步骤2：一键启动（在 repo 目录)
echo    docker compose build --no-cache backend
echo    docker compose -f compose.backend-only.yml up -d
echo.
echo 步骤3：打开浏览器
echo    Swagger API 文档: http://localhost:8000/docs
echo    Adminer 数据库: http://localhost:8080
echo.
echo 步骤4：测试 AI 摘要
echo    POST http://localhost:8000/api/v1/ai/summarize?text=这里写要总结的文本
echo.
echo 停止: docker compose -f compose.backend-only.yml down
echo 查看日志: docker compose -f compose.backend-only.yml logs -f backend
echo.
pause

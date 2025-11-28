@echo off
echo Running Backend Tests...
cd backend
call venv\Scripts\activate
pytest tests
if %errorlevel% neq 0 (
    echo Backend Tests Failed!
    exit /b %errorlevel%
)
deactivate
cd ..

echo.
echo Running Frontend Tests...
cd frontend
call npm run test:unit
if %errorlevel% neq 0 (
    echo Frontend Tests Failed!
    exit /b %errorlevel%
)
cd ..

echo.
echo All Tests Passed!

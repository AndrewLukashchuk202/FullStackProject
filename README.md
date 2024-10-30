# Project Setup Guide

This guide outlines the steps taken to set up a project that includes a Django backend and a Next.js frontend. The frontend captures mouse click coordinates and sends them to the backend, where the coordinates are printed to the console. Below are the detailed steps for setting up each part of the project.

## Step 1: Setting Up the Django Backend

1. **Create a Django Project**:
   - Install Django if you haven't already:
     ```bash
     pip install django
     ```
   - Create a new Django project:
     ```bash
     django-admin startproject helloworld
     cd helloworld
     ```

2. **Create a Django App**:
   - Create a new Django app within the project:
     ```bash
     python manage.py startapp appdjango
     ```

3. **Update Installed Apps**:
   - Open `settings.py` in the `helloworld` directory.
   - Add your new app to `INSTALLED_APPS`:
     ```python
     INSTALLED_APPS = [
         ...,
         'appdjango',
         'corsheaders',  # If you're using CORS
     ]
     ```

4. **Install Django CORS Headers**:
   - Install the CORS headers package to handle cross-origin requests:
     ```bash
     pip install django-cors-headers
     ```
   - Add `corsheaders` to your `INSTALLED_APPS` in `settings.py`.

5. **Configure Middleware**:
   - Add the CORS middleware to your `MIDDLEWARE` in `settings.py`:
     ```python
     MIDDLEWARE = [
         'corsheaders.middleware.CorsMiddleware',
         ...
     ]
     ```
   - Specify the allowed origins (the Next.js frontend URL):
     ```python
     CORS_ALLOWED_ORIGINS = [
         "http://localhost:3000",  # Next.js development server
     ]
     ```

6. **Create the API View**:
   - In `views.py` of the `appdjango` app, create a view to handle incoming POST requests:
     ```python
     from django.http import JsonResponse
     from django.views.decorators.csrf import csrf_exempt
     import json

     @csrf_exempt
     def send_coordinates(request):
         if request.method == 'POST':
             data = json.loads(request.body)
             x = data.get('x')
             y = data.get('y')
             print(f'Received coordinates: x={x}, y={y}')
             return JsonResponse({'status': 'success'})
         return JsonResponse({'status': 'error'}, status=400)
     ```

7. **Configure URLs**:
   - Create a `urls.py` file in the `appdjango` directory.
   - Define the URL pattern for your view:
     ```python
     from django.urls import path
     from .views import send_coordinates

     urlpatterns = [
         path('send-coordinates/', send_coordinates, name='send-coordinates'),
     ]
     ```

   - Include the app URLs in the main `urls.py`:
     ```python
     from django.contrib import admin
     from django.urls import path, include

     urlpatterns = [
         path('admin/', admin.site.urls),
         path('helloworld/', include('appdjango.urls')),
     ]
     ```

8. **Run the Django Server**:
   - Start the Django server to test the API:
     ```bash
     python manage.py runserver
     ```

## Step 2: Setting Up the Next.js Frontend

1. **Create a Next.js Project**:
   - In a new terminal window (outside the Django project directory), create a new Next.js project:
     ```bash
     npx create-next-app@latest my-next-app
     cd my-next-app
     ```

2. **Install Required Packages**:
   - Navigate to the project directory and install any additional packages if needed:
     ```bash
     npm install
     ```

3. **Create the Main Component**:
   - In the `src/app` directory, create a new folder (e.g., `some_folder`) for your components. 
   - Inside that folder, create a new file named `page.tsx` to handle the canvas and mouse click events:
     ```javascript
     // Import necessary libraries
     import React, { useEffect, useRef } from 'react';

     const AnimatedHelloWorld = () => {
         const canvasRef = useRef(null);

         // Handle mouse click event
         const handleClick = (event) => {
             const rect = canvasRef.current.getBoundingClientRect();
             const x = event.clientX - rect.left;
             const y = event.clientY - rect.top;
             sendClickDataToAPI(x, y);
         };

         const sendClickDataToAPI = (x, y) => {
             fetch('http://127.0.0.1:8000/helloworld/send-coordinates/', {
                 method: 'POST',
                 headers: {
                     'Content-Type': 'application/json',
                 },
                 body: JSON.stringify({ x, y }),
             })
             .then(response => response.json())
             .then(data => console.log('Success:', data))
             .catch((error) => console.error('Error:', error));
         };

         useEffect(() => {
             const canvas = canvasRef.current;
             canvas.addEventListener('click', handleClick);

             return () => {
                 canvas.removeEventListener('click', handleClick);
             };
         }, []);

         return <canvas ref={canvasRef} className="w-full h-full" />;
     };

     export default AnimatedHelloWorld;
     ```

4. **Accessing the Component**:
   - When you create a new script it's important that you call it - `page.tsx` file and also you can create a new folder within `src/app`, you can access it in your browser using the URL `http://localhost:3000/some_folder/`.

5. **Run the Next.js Development Server**:
   - Start the Next.js server:
     ```bash
     npm run dev
     ```

6. **Testing the Integration**:
   - Open the Next.js frontend in your browser (usually at `http://localhost:3000`).
   - Click on the canvas to send the coordinates to the Django backend.
   - Check the Django console to see the printed coordinates.

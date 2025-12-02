/**
 * Build script to inject Firebase config into cli-auth.html
 * Run this during the build process to replace placeholders with actual values
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read the template
const templatePath = path.join(__dirname, 'public', 'cli-auth.html');
const template = fs.readFileSync(templatePath, 'utf-8');

// Replace placeholders with environment variables
const config = {
    '__VITE_FIREBASE_API_KEY__': process.env.VITE_FIREBASE_API_KEY || '',
    '__VITE_FIREBASE_AUTH_DOMAIN__': process.env.VITE_FIREBASE_AUTH_DOMAIN || '',
    '__VITE_FIREBASE_PROJECT_ID__': process.env.VITE_FIREBASE_PROJECT_ID || '',
    '__VITE_FIREBASE_STORAGE_BUCKET__': process.env.VITE_FIREBASE_STORAGE_BUCKET || '',
    '__VITE_FIREBASE_MESSAGING_SENDER_ID__': process.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '',
    '__VITE_FIREBASE_APP_ID__': process.env.VITE_FIREBASE_APP_ID || ''
};

let output = template;
for (const [placeholder, value] of Object.entries(config)) {
    output = output.replace(new RegExp(placeholder, 'g'), value);
}

// Write to dist
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
}

const outputPath = path.join(distDir, 'cli-auth.html');
fs.writeFileSync(outputPath, output);

console.log('✅ Built cli-auth.html with Firebase config');

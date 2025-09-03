# CV Chequer Frontend

A modern React TypeScript frontend for the CV Chequer application built with Vite, Tailwind CSS, and modern UI patterns.

## Features

- **Modern React Development**: Built with React 18, TypeScript, and Vite for fast development
- **Responsive Design**: Mobile-first responsive design using Tailwind CSS
- **API Integration**: Full integration with CV Chequer FastAPI backend
- **File Upload**: Drag-and-drop file upload with validation
- **Real-time Analysis**: Live CV analysis with loading states and progress indicators
- **Error Handling**: Comprehensive error handling and user feedback
- **Navigation**: Modern sidebar navigation with routing

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **Lucide React** - Icon library

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── CVAnalysis/      # CV analysis specific components
│   ├── Layout/          # Layout components (Header, Sidebar, etc.)
│   └── UI/              # Generic UI components
├── pages/               # Page components
├── services/            # API services and configuration
├── types/               # TypeScript type definitions
├── utils/               # Utility functions and helpers
├── App.tsx              # Main application component
├── main.tsx             # Application entry point
└── index.css            # Global styles and Tailwind imports
```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=CV Chequer
VITE_APP_VERSION=1.0.0
```

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at http://localhost:3000

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The frontend communicates with the FastAPI backend through the API service located in `src/services/api.ts`. This service provides:

- **Health Check**: Monitor API connectivity
- **CV Analysis**: Upload and analyze single CV files
- **Job Matching**: Match CVs against job descriptions
- **Batch Processing**: Handle multiple files simultaneously
- **Job Analysis**: Extract requirements from job descriptions

### API Configuration

The API base URL is configured through environment variables. By default, it points to `http://localhost:8000`.

For production deployments, update the `VITE_API_BASE_URL` environment variable.

## Key Features

### CV Analysis
- Upload PDF files via drag-and-drop
- Real-time analysis progress
- Technology extraction with confidence scores
- Soft skills analysis with evidence
- Optional raw text extraction

### File Upload
- Drag-and-drop interface
- File validation (PDF only, size limits)
- Multiple file support for batch operations
- Progress indicators and error handling

### Responsive Design
- Mobile-first approach
- Sidebar navigation that collapses on mobile
- Responsive grid layouts
- Touch-friendly interactions

### Error Handling
- API connection monitoring
- User-friendly error messages
- Graceful fallbacks
- Loading states and spinners

## Development

### Code Style

The project uses ESLint and TypeScript for code quality:

- Follow React hooks best practices
- Use TypeScript for type safety
- Prefer functional components with hooks
- Use modern JavaScript features (ES6+)

### Components Architecture

- **Layout Components**: Handle application structure and navigation
- **UI Components**: Reusable, generic components
- **Feature Components**: Domain-specific components for CV analysis
- **Pages**: Top-level route components

### State Management

The application uses React's built-in state management:
- `useState` for local component state
- `useEffect` for side effects
- Custom hooks for shared logic
- Context API for global state (if needed)

## Building for Production

1. Build the application:
   ```bash
   npm run build
   ```

2. Preview the build:
   ```bash
   npm run preview
   ```

The built files will be in the `dist` directory.

## Deployment

The frontend can be deployed to any static hosting service:

- **Netlify**: Automatic deployments from Git
- **Vercel**: Zero-config deployments
- **AWS S3 + CloudFront**: Scalable static hosting
- **GitHub Pages**: Free hosting for public repositories

### Environment Configuration

Ensure proper environment variables are set for production:

```env
VITE_API_BASE_URL=https://your-api-domain.com
VITE_APP_NAME=CV Chequer
VITE_APP_VERSION=1.0.0
```

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new components
3. Include error handling for API calls
4. Test components on different screen sizes
5. Update documentation for new features

## Troubleshooting

### Common Issues

1. **API Connection Failed**: Ensure the backend server is running on the correct port
2. **File Upload Errors**: Check file size and format restrictions
3. **Build Errors**: Verify all dependencies are installed correctly
4. **Styling Issues**: Ensure Tailwind CSS is properly configured

### Development Tips

- Use the browser's network tab to debug API calls
- Check the console for error messages
- Use React Developer Tools for component inspection
- Test with different file sizes and formats
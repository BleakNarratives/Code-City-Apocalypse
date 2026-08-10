import React, { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error: error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="h-screen w-screen flex items-center justify-center bg-gray-900 text-white">
            <div className="p-8 text-red-400 bg-gray-800 rounded-lg shadow-xl">
                <h1 className="text-2xl font-bold mb-2">Something went wrong.</h1>
                <p>An unexpected error occurred. Please try refreshing the page.</p>
                <details className="mt-4 text-sm text-gray-400">
                    <summary>Error Details</summary>
                    <pre className="mt-2 p-2 bg-gray-900 rounded overflow-auto">
                        {this.state.error?.toString()}
                    </pre>
                </details>
            </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

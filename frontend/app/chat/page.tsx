'use client';

import { useState } from 'react';
import DashboardLayout from '@/components/layout/dashboard-layout';
import { Button } from '@/components/ui/button';
import { useSendMessage, useChatSuggestions } from '@/hooks';

interface Message {
  id: string;
  content: string;
  type: 'user' | 'assistant';
  timestamp: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content:
        "Hello! I'm your AI assistant. I can help you analyze your business data, generate reports, and provide insights. What would you like to know?",
      type: 'assistant',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [sessionId] = useState(() => `session-${Date.now()}`);

  const sendMessageMutation = useSendMessage();
  const { data: suggestions } = useChatSuggestions();

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || sendMessageMutation.isPending) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue.trim(),
      type: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');

    try {
      const response = await sendMessageMutation.mutateAsync({
        message: userMessage.content,
        conversationId: sessionId,
        context: JSON.stringify({
          previousMessages: messages.slice(-5), // Send last 5 messages for context
        }),
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content:
          response.message ||
          'I apologize, but I encountered an issue processing your request.',
        type: 'assistant',
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content:
          "I'm sorry, I encountered an error while processing your request. Please try again.",
        type: 'assistant',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion);
  };

  return (
    <DashboardLayout>
      <div className="flex h-[calc(100vh-8rem)] max-w-7xl mx-auto">
        {/* Chat Area */}
        <div className="flex-1 flex flex-col bg-white rounded-lg shadow">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <div>
              <h1 className="text-xl font-semibold text-gray-900">
                AI Assistant
              </h1>
              <p className="text-sm text-gray-500">
                Ask me anything about your business
              </p>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex h-2 w-2 rounded-full bg-green-400"></div>
              <span className="text-sm text-gray-500">Online</span>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="text-sm">{message.content}</p>
                  <p
                    className={`text-xs mt-1 ${
                      message.type === 'user'
                        ? 'text-blue-100'
                        : 'text-gray-500'
                    }`}
                  >
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
            {sendMessageMutation.isPending && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div
                        className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0.1s' }}
                      ></div>
                      <div
                        className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0.2s' }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-500">
                      AI is thinking...
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 p-4">
            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 min-w-0 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                disabled={sendMessageMutation.isPending}
              />
              <Button
                type="submit"
                disabled={!inputValue.trim() || sendMessageMutation.isPending}
                loading={sendMessageMutation.isPending}
              >
                Send
              </Button>
            </form>
          </div>
        </div>

        {/* Suggestions Sidebar */}
        <div className="w-80 ml-4 bg-white rounded-lg shadow p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Suggested Questions
          </h3>

          {suggestions && suggestions.length > 0 ? (
            <div className="space-y-2">
              {suggestions.map((suggestion: any, index: number) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion.text)}
                  className="w-full text-left p-3 text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors"
                >
                  {suggestion.text}
                </button>
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              <button
                onClick={() =>
                  handleSuggestionClick(
                    'What are our top sales metrics for this month?'
                  )
                }
                className="w-full text-left p-3 text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors"
              >
                What are our top sales metrics for this month?
              </button>
              <button
                onClick={() =>
                  handleSuggestionClick(
                    'Show me our financial performance summary'
                  )
                }
                className="w-full text-left p-3 text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors"
              >
                Show me our financial performance summary
              </button>
              <button
                onClick={() =>
                  handleSuggestionClick('How is our HR team performing?')
                }
                className="w-full text-left p-3 text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors"
              >
                How is our HR team performing?
              </button>
              <button
                onClick={() =>
                  handleSuggestionClick('Generate a quarterly business report')
                }
                className="w-full text-left p-3 text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors"
              >
                Generate a quarterly business report
              </button>
              <button
                onClick={() =>
                  handleSuggestionClick(
                    'What trends do you see in our customer data?'
                  )
                }
                className="w-full text-left p-3 text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors"
              >
                What trends do you see in our customer data?
              </button>
            </div>
          )}

          <div className="mt-6 pt-6 border-t border-gray-200">
            <h4 className="text-sm font-medium text-gray-900 mb-2">
              Quick Actions
            </h4>
            <div className="space-y-2">
              <Button
                variant="outline"
                size="sm"
                className="w-full justify-start"
              >
                <svg
                  className="h-4 w-4 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                New Report
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="w-full justify-start"
              >
                <svg
                  className="h-4 w-4 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"
                  />
                </svg>
                Export Data
              </Button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}


import React, { useState, useEffect, useRef } from 'react';
import { GoogleGenAI, Chat } from '@google/genai';
import { Message, Role } from './types.ts';
import Header from './components/Header.tsx';
import ChatWindow from './components/ChatWindow.tsx';
import InputBar from './components/InputBar.tsx';
import { SYSTEM_INSTRUCTION } from './constants.ts';

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const chatRef = useRef<Chat | null>(null);

  useEffect(() => {
    // Initialize chat and add welcome message
    const initializeChat = () => {
      try {
        if (!process.env.API_KEY) {
          throw new Error("API_KEY environment variable not set.");
        }
        const ai = new GoogleGenAI({ apiKey: process.env.API_KEY, vertexai: true });
        chatRef.current = ai.chats.create({
          model: 'gemini-2.5-flash',
          config: {
            systemInstruction: SYSTEM_INSTRUCTION,
          },
        });
        setMessages([
          {
            role: 'model',
            content: "Welcome to Stratos Assistant. I am a guide for our automated hedging bots and account services. How can I help you today?",
            timestamp: new Date(),
          },
        ]);
      } catch (e) {
        console.error("Initialization failed:", e);
        const errorMessage = e instanceof Error ? e.message : "An unknown error occurred during initialization.";
        setError(`Failed to initialize the assistant. Please ensure your API key is configured correctly. Error: ${errorMessage}`);
      }
    };
    initializeChat();
  }, []);

  const handleSendMessage = async (inputText: string) => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: inputText,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      if (!chatRef.current) {
        throw new Error("Chat is not initialized.");
      }
      
      const response = await chatRef.current.sendMessage({ message: inputText });
      
      const modelMessage: Message = {
        role: 'model',
        content: response.text,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, modelMessage]);

    } catch (e) {
      console.error("Error sending message:", e);
      const errorMessageContent = e instanceof Error ? e.message : "An unknown error occurred.";
      const errorMessage: Message = {
        role: 'model',
        content: `Sorry, I encountered an error. Please try again. Details: ${errorMessageContent}`,
        timestamp: new Date(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-h-screen bg-slate-900">
      <Header />
      <main className="flex-1 overflow-hidden">
        <ChatWindow messages={messages} isLoading={isLoading} />
      </main>
      <div className="p-4 bg-slate-900/80 backdrop-blur-sm border-t border-slate-700">
        {error && (
          <div className="text-center text-red-400 mb-2 text-sm">
            {error}
          </div>
        )}
        <InputBar onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default App;

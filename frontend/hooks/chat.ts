import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';

export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  conversationId?: string;
  metadata?: {
    confidence?: number;
    suggestions?: string[];
    context?: string;
  };
}

export interface SendMessageRequest {
  message: string;
  conversationId?: string;
  context?: string;
}

export interface Conversation {
  id: string;
  title: string;
  lastMessage?: string;
  lastMessageAt: Date;
  messageCount: number;
}

export interface ChatSuggestion {
  id: string;
  text: string;
  category: 'general' | 'analysis' | 'reporting' | 'support';
  prompt: string;
}

// Send message mutation
export const useSendMessage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: SendMessageRequest) => {
      const response = await api.post('/chat/messages', data);
      return response.data;
    },
    onSuccess: (data, variables) => {
      // Update messages cache
      queryClient.setQueryData(
        ['chat', 'messages', variables.conversationId],
        (old: ChatMessage[] | undefined) => {
          return old ? [...old, data] : [data];
        }
      );

      // Invalidate conversations to update last message
      queryClient.invalidateQueries({ queryKey: ['chat', 'conversations'] });
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Failed to send message');
    },
  });
};

// Get chat messages query
export const useChatMessages = (conversationId: string | undefined) => {
  return useQuery({
    queryKey: ['chat', 'messages', conversationId],
    queryFn: async () => {
      if (!conversationId) return [];
      const response = await api.get(
        `/chat/conversations/${conversationId}/messages`
      );
      return response.data;
    },
    enabled: !!conversationId,
    staleTime: 30 * 1000, // 30 seconds
  });
};

// Get conversations query
export const useConversations = () => {
  return useQuery({
    queryKey: ['chat', 'conversations'],
    queryFn: async () => {
      const response = await api.get('/chat/conversations');
      return response.data;
    },
    staleTime: 60 * 1000, // 1 minute
  });
};

// Create new conversation mutation
export const useCreateConversation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (title: string) => {
      const response = await api.post('/chat/conversations', { title });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat', 'conversations'] });
    },
    onError: (error: any) => {
      toast.error(
        error?.response?.data?.detail || 'Failed to create conversation'
      );
    },
  });
};

// Delete conversation mutation
export const useDeleteConversation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (conversationId: string) => {
      const response = await api.delete(
        `/chat/conversations/${conversationId}`
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat', 'conversations'] });
    },
    onError: (error: any) => {
      toast.error(
        error?.response?.data?.detail || 'Failed to delete conversation'
      );
    },
  });
};

// Get chat suggestions query
export const useChatSuggestions = () => {
  return useQuery({
    queryKey: ['chat', 'suggestions'],
    queryFn: async () => {
      const response = await api.get('/chat/suggestions');
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Get AI insights mutation (for more complex analysis)
export const useGetAIInsights = () => {
  return useMutation({
    mutationFn: async (query: string) => {
      const response = await api.post('/ai/insights', { query });
      return response.data;
    },
    onError: (error: any) => {
      toast.error(error?.response?.data?.detail || 'Failed to get AI insights');
    },
  });
};

// Export conversation mutation
export const useExportConversation = () => {
  return useMutation({
    mutationFn: async (conversationId: string) => {
      const response = await api.get(
        `/chat/conversations/${conversationId}/export`,
        {
          responseType: 'blob',
        }
      );
      return response.data;
    },
    onSuccess: (data, conversationId) => {
      // Create download link
      const url = window.URL.createObjectURL(new Blob([data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `conversation-${conversationId}.json`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      toast.success('Conversation exported successfully');
    },
    onError: (error: any) => {
      toast.error(
        error?.response?.data?.detail || 'Failed to export conversation'
      );
    },
  });
};

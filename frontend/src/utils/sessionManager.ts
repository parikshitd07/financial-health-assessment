/**
 * Session Manager - Creates and manages anonymous user sessions
 * Sessions expire after 1 hour and data is cleared
 */

interface SessionData {
  sessionId: string;
  userId: number;
  businessId: number;
  createdAt: number;
  expiresAt: number;
}

const SESSION_DURATION = 60 * 60 * 1000; // 1 hour in milliseconds
const SESSION_KEY = 'fha_session';

export class SessionManager {
  /**
   * Get or create a session
   */
  static getSession(): SessionData {
    const stored = localStorage.getItem(SESSION_KEY);
    
    if (stored) {
      try {
        const session: SessionData = JSON.parse(stored);
        
        // Check if session is still valid
        if (Date.now() < session.expiresAt) {
          return session;
        } else {
          // Session expired, clear it
          this.clearSession();
        }
      } catch (e) {
        // Invalid session data, clear it
        this.clearSession();
      }
    }
    
    // Create new session
    return this.createNewSession();
  }
  
  /**
   * Create a new anonymous session
   */
  private static createNewSession(): SessionData {
    const now = Date.now();
    const sessionId = this.generateSessionId();
    
    const session: SessionData = {
      sessionId,
      userId: 1, // Default anonymous user
      businessId: 1, // Default business
      createdAt: now,
      expiresAt: now + SESSION_DURATION
    };
    
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return session;
  }
  
  /**
   * Update business ID in session
   */
  static updateBusinessId(businessId: number): void {
    const session = this.getSession();
    session.businessId = businessId;
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }
  
  /**
   * Clear session and all related data
   */
  static clearSession(): void {
    localStorage.removeItem(SESSION_KEY);
    // Clear any other cached data
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
  
  /**
   * Check if session is expired
   */
  static isSessionExpired(): boolean {
    const stored = localStorage.getItem(SESSION_KEY);
    if (!stored) return true;
    
    try {
      const session: SessionData = JSON.parse(stored);
      return Date.now() >= session.expiresAt;
    } catch {
      return true;
    }
  }
  
  /**
   * Get time remaining in session (in minutes)
   */
  static getTimeRemaining(): number {
    const session = this.getSession();
    const remaining = session.expiresAt - Date.now();
    return Math.max(0, Math.floor(remaining / 60000)); // Convert to minutes
  }
  
  /**
   * Generate a unique session ID
   */
  private static generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  /**
   * Extend session by another hour
   */
  static extendSession(): void {
    const session = this.getSession();
    session.expiresAt = Date.now() + SESSION_DURATION;
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }
}

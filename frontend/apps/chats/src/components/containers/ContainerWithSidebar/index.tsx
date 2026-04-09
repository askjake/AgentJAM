import { FC } from 'react';
import { Layout } from 'antd';
import dynamic from 'next/dynamic';

import CustomHeader from '../../organisms/Headers/CustomHeader';
import {
  StyledContainerWithSidebar,
  StyledContainerWithSidebarContent,
} from '@/components/containers/ContainerWithSidebar/ContainerWithSidebar.styled';
import CustomFooter from '@shared/ui/components/organisms/Footers/CustomFooter';
import CustomSidebar from '../../organisms/Sidebars/CustomSidebar';

import { ContainerWithSidebarProps } from '@/components/containers/ContainerWithSidebar/ContainerWithSidebar.props';

// ==============================================================================
// NEW ADDITION: QuickAccessFAB Component
// ==============================================================================
// Floating Action Button that provides quick access to:
// - Settings page
// - LLM Configuration
// - Learning Journal
// - Thought Visualizer
// 
// Positioned at bottom-right of the screen, always accessible.
// Dynamically imported to optimize initial page load.
// ==============================================================================
const QuickAccessFAB = dynamic(
  () => import('@/components/molecules/QuickAccessFAB'),
  {
    ssr: false, // Client-side only (uses router hooks)
  },
);

// ==============================================================================
// ContainerWithSidebar Component
// ==============================================================================
// Main layout container that provides the application structure:
// - CustomSidebar: Left sidebar with navigation
// - CustomHeader: Top header with controls
// - Content: Main content area (children)
// - CustomFooter: Bottom footer
// - QuickAccessFAB: Floating action button (NEW)
// ==============================================================================
const ContainerWithSidebar: FC<ContainerWithSidebarProps> = ({
  showChats = false,
  children,
}) => {
  return (
    <StyledContainerWithSidebar hasSider>
      {/* ====================================================================== */}
      {/* Left Sidebar */}
      {/* ====================================================================== */}
      {/* Contains chat list, apps, and primary navigation */}
      {/* ====================================================================== */}
      <CustomSidebar showChats={showChats} />
      
      {/* ====================================================================== */}
      {/* Main Content Area */}
      {/* ====================================================================== */}
      <Layout>
        {/* Top Header: Contains title, controls, and user menu */}
        <CustomHeader showChats={showChats} />
        
        {/* Main Content: Page-specific content rendered here */}
        <StyledContainerWithSidebarContent>
          {children}
        </StyledContainerWithSidebarContent>
        
        {/* Bottom Footer: App information and links */}
        <CustomFooter />
      </Layout>
      
      {/* ====================================================================== */}
      {/* NEW: Quick Access Floating Action Button */}
      {/* ====================================================================== */}
      {/* Fixed position button in bottom-right corner */}
      {/* Provides quick navigation to frequently used features: */}
      {/*   - ⚙️ Settings */}
      {/*   - 🤖 LLM Configuration */}
      {/*   - 📝 Learning Journal */}
      {/*   - 💡 Thought Visualizer */}
      {/* */}
      {/* The FAB appears on top of all content (high z-index) */}
      {/* and is always accessible regardless of scroll position. */}
      {/* */}
      {/* Position: right: 24px, bottom: 24px */}
      {/* Type: Primary (blue theme color) */}
      {/* Trigger: Click to expand menu */}
      {/* ====================================================================== */}
      <QuickAccessFAB />
    </StyledContainerWithSidebar>
  );
};

export default ContainerWithSidebar;


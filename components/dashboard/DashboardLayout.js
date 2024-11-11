import React from 'react';
import { FileText, ExternalLink, Download, LogOut, Settings, User } from 'lucide-react';

const DashboardLayout = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-blue-600">MyDocs Portal</h1>
        </div>
        
        <nav className="mt-6">
          <div className="px-4 space-y-2">
            <a href="#profile" className="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 rounded-lg">
              <User className="h-5 w-5 mr-3" />
              <span>Προφίλ</span>
            </a>
            <a href="#services" className="flex items-center px-4 py-3 text-blue-600 bg-blue-50 rounded-lg">
              <FileText className="h-5 w-5 mr-3" />
              <span>Υπηρεσίες</span>
            </a>
            <a href="#settings" className="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 rounded-lg">
              <Settings className="h-5 w-5 mr-3" />
              <span>Ρυθμίσεις</span>
            </a>
            <a href="#logout" className="flex items-center px-4 py-3 text-gray-700 hover:bg-blue-50 rounded-lg">
              <LogOut className="h-5 w-5 mr-3" />
              <span>Έξοδος</span>
            </a>
          </div>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Υπεύθυνη Δήλωση Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <FileText className="h-8 w-8 text-blue-600" />
              <h2 className="text-xl font-semibold ml-3">Υπεύθυνη Δήλωση</h2>
            </div>
            <p className="text-gray-600 mb-4">Δημιουργία και λήψη υπεύθυνης δήλωσης</p>
            <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
              Έναρξη
            </button>
          </div>

          {/* Εξουσιοδότηση Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <ExternalLink className="h-8 w-8 text-blue-600" />
              <h2 className="text-xl font-semibold ml-3">Εξουσιοδότηση</h2>
            </div>
            <p className="text-gray-600 mb-4">Δημιουργία και λήψη εξουσιοδότησης</p>
            <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
              Έναρξη
            </button>
          </div>

          {/* Βεβαίωση Ανεργίας Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <Download className="h-8 w-8 text-blue-600" />
              <h2 className="text-xl font-semibold ml-3">Βεβαίωση Ανεργίας</h2>
            </div>
            <p className="text-gray-600 mb-4">Λήψη βεβαίωσης ανεργίας</p>
            <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
              Έναρξη
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;

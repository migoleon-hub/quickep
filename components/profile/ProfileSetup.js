import React, { useState } from 'react';
import { User, Lock, Download, Save, AlertCircle } from 'lucide-react';


const ProfileSetup = () => {
  const [isManual, setIsManual] = useState(true);
  const [saveTaxisnetCreds, setSaveTaxisnetCreds] = useState(false);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [errors, setErrors] = useState({});
  
  const [formData, setFormData] = useState({
  	// Βασικά στοιχεία
  	firstName: '',
  	lastName: '',
  	fatherName: '',
  	motherName: '',
  	birthDate: '',
  	birthPlace: '',
  	
  	// Στοιχεία ταυτοποίησης
  	idType: '',
  	idNumber: '',
  	idIssueDate: '',
  	idIssueAuthority: '',
  	
  	// ΑΦΜ/ΑΜΚΑ
  	afm: '',
  	amka: '',
  	doy: '',
  	
  	// Διεύθυνση
  	street: '',           // αλλαγή από address
  	streetNumber: '',     // αλλαγή από number
  	city: '',
  	postalCode: '',
  	
  	// Taxisnet credentials
  	taxisnetUsername: '',
  	taxisnetPassword: ''
  });



  // Πρόσθεσε αυτά κάτω από τα imports
  const validateAFM = (afm) => {
    const afmRegex = /^\d{9}$/;
    if (!afmRegex.test(afm)) {
      return 'Το ΑΦΜ πρέπει να αποτελείται από 9 ψηφία';
    }
    return '';
  };
  
  const validateAMKA = (amka) => {
    const amkaRegex = /^\d{11}$/;
    if (!amkaRegex.test(amka)) {
      return 'Το ΑΜΚΑ πρέπει να αποτελείται από 11 ψηφία';
    }
    return '';
  };
  
  const validateRequired = (value, fieldName) => {
    if (!value || value.trim() === '') {
      return `Το πεδίο ${fieldName} είναι υποχρεωτικό`;
    }
    return '';
  };

  const handleTaxisnetSync = async () => {
    try {
      setLoading(true);
      const credentials = {
        username: formData.taxisnetUsername,
        password: formData.taxisnetPassword
      };

      const response = await fetch('/api/fetch-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      });

      const data = await response.json();
      
      if (data.success) {
        // Update form with fetched data
        setFormData(prevData => ({
          ...prevData,
          firstName: data.data.fullname.split(' ')[1],
          lastName: data.data.fullname.split(' ')[0],
          fatherName: data.data.fathername,
          motherName: data.data.mothername,
          birthPlace: data.data.birthplace,
          birthDate: data.data.birth_date,
          idType: data.data.id_type,
          idNumber: data.data.id_number,
          afm: data.data.afm,
          doy: data.data.doy,
          street: data.data.address.street,
          streetNumber: data.data.address.number,
          city: data.data.address.city,
          postalCode: data.data.address.postal_code,
          // Keep credentials if user chose to save them
          taxisnetUsername: saveTaxisnetCreds ? formData.taxisnetUsername : '',
          taxisnetPassword: saveTaxisnetCreds ? formData.taxisnetPassword : ''
        }));
        setStatusMessage('Τα στοιχεία ανακτήθηκαν επιτυχώς!');
      } else {
        setStatusMessage('Σφάλμα κατά την ανάκτηση στοιχείων');
      }
    } catch (error) {
      setStatusMessage('Σφάλμα σύνδεσης με το Taxisnet');
    } finally {
      setLoading(false);
    }
  };


  // Πρόσθεσε τη συνάρτηση validation πριν το handleManualSubmit
  const validateForm = () => {
    const newErrors = {};
    
    // Βασικά στοιχεία
    newErrors.lastName = validateRequired(formData.lastName, 'Επώνυμο');
    newErrors.firstName = validateRequired(formData.firstName, 'Όνομα');
    newErrors.fatherName = validateRequired(formData.fatherName, 'Πατρώνυμο');
    newErrors.motherName = validateRequired(formData.motherName, 'Μητρώνυμο');
    
    // Στοιχεία Ταυτότητας
    newErrors.idType = validateRequired(formData.idType, 'Τύπος Εγγράφου');
    newErrors.idNumber = validateRequired(formData.idNumber, 'Αριθμός Ταυτότητας');
    
    // ΑΦΜ/ΑΜΚΑ
    newErrors.afm = validateAFM(formData.afm);
    newErrors.amka = validateAMKA(formData.amka);
    
    // Διεύθυνση
    newErrors.street = validateRequired(formData.street, 'Οδός');
    newErrors.streetNumber = validateRequired(formData.streetNumber, 'Αριθμός');
    newErrors.city = validateRequired(formData.city, 'Πόλη');
    newErrors.postalCode = validateRequired(formData.postalCode, 'Τ.Κ.');
    
    // Καθαρίζουμε τα κενά errors
    Object.keys(newErrors).forEach(key => {
      if (!newErrors[key]) {
        delete newErrors[key];
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) {
      setStatusMessage('Παρακαλώ διορθώστε τα σφάλματα στη φόρμα');
      return;
    }
    try {
      setLoading(true);
      const response = await fetch('/api/profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
  
      const data = await response.json();
      if (data.success) {
        setStatusMessage('Τα στοιχεία αποθηκεύτηκαν επιτυχώς!');
      } else {
        setStatusMessage('Σφάλμα κατά την αποθήκευση των στοιχείων');
      }
    } catch (error) {
      setStatusMessage('Σφάλμα επικοινωνίας με τον server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-2xl font-bold mb-6">Ρύθμιση Προφίλ</h1>
        
        {/* Data Entry Selection */}
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setIsManual(true)}
            className={`flex-1 p-4 rounded-lg border-2 ${
              isManual ? 'border-blue-600 bg-blue-50' : 'border-gray-200'
            }`}
          >
            <User className="w-6 h-6 mb-2 mx-auto" />
            <h3 className="font-semibold">Χειροκίνητη Καταχώρηση</h3>
          </button>
          
          <button
            onClick={() => setIsManual(false)}
            className={`flex-1 p-4 rounded-lg border-2 ${
              !isManual ? 'border-blue-600 bg-blue-50' : 'border-gray-200'
            }`}
          >
            <Lock className="w-6 h-6 mb-2 mx-auto" />
            <h3 className="font-semibold">Σύνδεση με TAXISnet</h3>
          </button>
        </div>

        {!isManual ? (
          // Taxisnet Integration Form
          <div className="space-y-6">
            <div className="bg-blue-50 p-4 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5" />
              <p className="text-sm text-blue-800">
                Τα στοιχεία σας θα ανακτηθούν αυτόματα από το TAXISnet. 
                Παρακαλώ εισάγετε τα διαπιστευτήριά σας.
              </p>
            </div>
            
            <div className="grid grid-cols-1 gap-6">
              <div>
                <label className="block text-sm font-medium mb-1">Username Taxisnet</label>
                <input
                  type="text"
                  className="w-full p-3 border rounded-lg"
                  value={formData.taxisnetUsername}
                  onChange={(e) => setFormData({...formData, taxisnetUsername: e.target.value})}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Password Taxisnet</label>
                <input
                  type="password"
                  className="w-full p-3 border rounded-lg"
                  value={formData.taxisnetPassword}
                  onChange={(e) => setFormData({...formData, taxisnetPassword: e.target.value})}
                />
              </div>
              
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="saveCreds"
                  className="w-4 h-4 text-blue-600"
                  checked={saveTaxisnetCreds}
                  onChange={(e) => setSaveTaxisnetCreds(e.target.checked)}
                />
                <label htmlFor="saveCreds" className="text-sm text-gray-600">
                  Αποθήκευση διαπιστευτηρίων για μελλοντική χρήση
                </label>
              </div>
            </div>
            
            {statusMessage && (
              <div className={`p-4 rounded-lg ${
                statusMessage.includes('επιτυχώς') 
                  ? 'bg-green-50 text-green-800' 
                  : 'bg-red-50 text-red-800'
              }`}>
                {statusMessage}
              </div>
            )}
            
            <button
              onClick={handleTaxisnetSync}
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                  Γίνεται ανάκτηση...
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  Αυτόματη Άντληση Δεδομένων
                </>
              )}
            </button>
          </div>
        ) : (
          // Manual Form
          <form className="space-y-6" onSubmit={handleManualSubmit}>
            {/* Προσωπικά Στοιχεία */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Προσωπικά Στοιχεία</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Επώνυμο</label>
                  <input
                    type="text"
                    className="w-full p-2 border rounded-lg"
                    value={formData.lastName}
                    onChange={(e) => setFormData({...formData, lastName: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Όνομα</label>
                  <input
                    type="text"
                    className="w-full p-2 border rounded-lg"
                    value={formData.firstName}
                    onChange={(e) => setFormData({...formData, firstName: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Πατρώνυμο</label>
                  <input
                    type="text"
                    className="w-full p-2 border rounded-lg"
                    value={formData.fatherName}
                    onChange={(e) => setFormData({...formData, fatherName: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Μητρώνυμο</label>
                  <input
                    type="text"
                    className="w-full p-2 border rounded-lg"
                    value={formData.motherName}
                    onChange={(e) => setFormData({...formData, motherName: e.target.value})}
                  />
                </div>
              </div>
            </div>

            {/* Στοιχεία Γέννησης */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Στοιχεία Γέννησης</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Ημερομηνία Γέννησης</label>
                  <input
                    type="date"
                    className="w-full p-2 border rounded-lg"
                    value={formData.birthDate}
                    onChange={(e) => setFormData({...formData, birthDate: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Τόπος Γέννησης</label>
                  <input
                    type="text"
                    className="w-full p-2 border rounded-lg"
                    value={formData.birthPlace}
                    onChange={(e) => setFormData({...formData, birthPlace: e.target.value})}
                  />
                </div>
              </div>
            </div>

            {/* Στοιχεία Ταυτότητας */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Στοιχεία Ταυτότητας</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Τύπος Εγγράφου</label>
                  <select
                    className="w-full p-2 border rounded-lg"
                    value={formData.idType}
                    onChange={(e) => setFormData({...formData, idType: e.target.value})}
                  >
                    <option value="">Επιλέξτε...</option>
                    <option value="id">Δελτίο Ταυτότητας</option>
                    <option value="passport">Διαβατήριο</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Αριθμός</label>
                  <input
                    type="text"
                    className="w-full p-2 border rounded-lg"
                    value={formData.idNumber}
                    onChange={(e) => setFormData({...formData, idNumber: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Ημ/νία Έκδοσης</label>
                  <input
                    type="date"
                    className="w-full p-2 border rounded-lg"
                    value={formData.idIssueDate}
                    onChange={(e) => setFormData({...formData, idIssueDate: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Εκδούσα Αρχή</label>
                  <input
                    type="text"
                    className="w-full p-2 border rounded-lg"
                    value={formData.idIssueAuthority}
                    onChange={(e) => setFormData({...formData, idIssueAuthority: e.target.value})}
                  />
                </div>
              </div>
            </div>

            {/* ΑΦΜ/ΑΜΚΑ/ΔΟΥ */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Στοιχεία ΑΦΜ/ΑΜΚΑ</h3>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">ΑΦΜ</label>
                  <input
                    type="text"
                    className="w-full p-2 border rounded-lg"
					value={formData.afm}
					onChange={(e) => setFormData({...formData, afm: e.target.value})}
					/>
				</div>
			<div>
				  <label className="block text-sm font-medium mb-1">ΑΜΚΑ</label>
				  <input
					type="text"
					className="w-full p-2 border rounded-lg"
					value={formData.amka}
					onChange={(e) => setFormData({...formData, amka: e.target.value})}
				  />
				</div>
				<div>
				  <label className="block text-sm font-medium mb-1">ΔΟΥ</label>
				  <input
					type="text"
					className="w-full p-2 border rounded-lg"
					value={formData.doy}
					onChange={(e) => setFormData({...formData, doy: e.target.value})}
				  />
				</div>
				</div>

				{/* Διεύθυνση */}
				<div className="space-y-4 mt-6">
				  <h3 className="text-lg font-semibold">Στοιχεία Διεύθυνσης</h3>
				  <div className="grid grid-cols-6 gap-4">
					<div className="col-span-3">
					  <label className="block text-sm font-medium mb-1">Οδός</label>
					  <input
						type="text"
						className="w-full p-2 border rounded-lg"
						value={formData.street}
						onChange={(e) => setFormData({...formData, street: e.target.value})}
					  />
					</div>
					<div>
					  <label className="block text-sm font-medium mb-1">Αριθμός</label>
					  <input
						type="text"
						className="w-full p-2 border rounded-lg"
						value={formData.streetNumber}
						onChange={(e) => setFormData({...formData, streetNumber: e.target.value})}
					  />
					</div>
					<div>
					  <label className="block text-sm font-medium mb-1">Τ.Κ.</label>
					  <input
						type="text"
						className="w-full p-2 border rounded-lg"
						value={formData.postalCode}
						onChange={(e) => setFormData({...formData, postalCode: e.target.value})}
					  />
					</div>
					<div>
					  <label className="block text-sm font-medium mb-1">Πόλη</label>
					  <input
						type="text"
						className="w-full p-2 border rounded-lg"
						value={formData.city}
						onChange={(e) => setFormData({...formData, city: e.target.value})}
					  />
					</div>
				  </div>
				</div>

				{/* Taxisnet Credentials */}
				{!isManual && (
				  <div className="space-y-4 mt-6">
					<h3 className="text-lg font-semibold">Στοιχεία Taxisnet</h3>
					<div className="grid grid-cols-2 gap-4">
					  <div>
						<label className="block text-sm font-medium mb-1">Username</label>
						<input
						  type="text"
						  className="w-full p-2 border rounded-lg"
						  value={formData.taxisnetUsername}
						  onChange={(e) => setFormData({...formData, taxisnetUsername: e.target.value})}
						/>
					  </div>
					  <div>
						<label className="block text-sm font-medium mb-1">Password</label>
						<input
						  type="password"
						  className="w-full p-2 border rounded-lg"
						  value={formData.taxisnetPassword}
						  onChange={(e) => setFormData({...formData, taxisnetPassword: e.target.value})}
						/>
					  </div>
					</div>
					
					{/* Save Credentials Checkbox */}
					<div className="flex items-center mt-4">
					  <input
						type="checkbox"
						id="saveCreds"
						className="w-4 h-4 text-blue-600"
						checked={saveTaxisnetCreds}
						onChange={(e) => setSaveTaxisnetCreds(e.target.checked)}
					  />
					  <label htmlFor="saveCreds" className="ml-2 text-sm text-gray-600">
						Αποθήκευση διαπιστευτηρίων Taxisnet για μελλοντική χρήση
					  </label>
					</div>
				  </div>
				)}

				{/* Submit Button */}
				<div className="mt-8">
				  {isManual ? (
					<button 
					  type="submit" 
					  disabled={loading}
					  className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 flex items-center justify-center"
					>
					  {loading ? (
					    <>
					      <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
					      Αποθήκευση...
					    </>
					  ) : (
					    <>
					      <Save className="w-5 h-5 mr-2" />
					      Αποθήκευση Στοιχείων
					    </>
					  )}
					</button>
				  )}
				</div>
			  </form>   
			)}         
		  </div>      
		</div>        
	  );           
	};           

export default ProfileSetup;

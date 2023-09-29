import React, { useState, useEffect } from "react";
// import db from "../../data/db";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "bootstrap/dist/css/bootstrap.min.css";

function Appointments() {
  const [especializacion, setEspecializacion] = useState("");
  const [especializaciones, setEspecializaciones] = useState([]);
  const [doctoresEncontrados, setDoctoresEncontrados] = useState([]);
  const [doctor, setDoctor] = useState("");
  const [dia, setDia] = useState(new Date());
  const [hora, setHora] = useState("");

  // useEffect(() => {
  //   // Llama a buscarEspecializacion cuando el componente se monta para obtener las especializaciones existentes
  //   buscarEspecializacion();
  // }, []); // El segundo argumento vacío [] indica que esto solo se ejecuta una vez cuando el componente se monta

  // const buscarEspecializacion = () => {
  //   const especializacionesExistentes = [
  //     ...new Set(db.doctores.map((doc) => doc.especializacion)),
  //   ];

  //   if (especializacionesExistentes.length > 0) {
  //     setEspecializaciones(especializacionesExistentes);
  //   } else {
  //     setEspecializaciones([]);
  //   }
  // };

  // const buscarDoctoresPorEspecializacion = (especializacionSeleccionada) => {
  //   const doctoresPorEspecializacion = db.doctores.filter(
  //     (doc) => doc.especializacion === especializacionSeleccionada
  //   );

  //   if (doctoresPorEspecializacion.length > 0) {
  //     setDoctoresEncontrados(doctoresPorEspecializacion);
  //   } else {
  //     setDoctoresEncontrados([]);
  //   }
  // };

  // const handleEspecializacionChange = (e) => {
  //   setEspecializacion(e.target.value);
  //   setDoctor(""); // Restablecer el valor del doctor al cambiar la especialización
  //   buscarDoctoresPorEspecializacion(e.target.value);
  // };

  // const solicitarCita = () => {
  //   const nuevaCita = {
  //     especializacion,
  //     doctor,
  //     dia,
  //     hora,
  //   };
  //   db.citasMedicas.push(nuevaCita);
  //   console.log("Cita solicitada:", nuevaCita);
  // };

  // const generarHoras = () => {
  //   const horas = [];
  //   for (let i = 0; i < 24; i++) {
  //     for (let j = 0; j < 60; j += 15) {
  //       const horaFormateada = `${String(i).padStart(2, "0")}:${String(
  //         j
  //       ).padStart(2, "0")}`;
  //       horas.push(horaFormateada);
  //     }
  //   }
  //   return horas;
  // };

  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">Pedir Citas Médicas</h2>
      <form>
        <div className="row mb-3">
          <div className="col-md-6">
            <label htmlFor="especializacion" className="form-label">
              Especialización
            </label>
            <select
              // value={especializacion}
              // onChange={handleEspecializacionChange}
              className="form-select"
              id="especializacion"
            >
              <option value="">Selecciona Especialización</option>
              {especializaciones.map((especializacion) => (
                <option key={especializacion} value={especializacion}>
                  {especializacion}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label htmlFor="doctor" className="form-label">
              Doctor
            </label>
            <select
              value={doctor}
              onChange={(e) => setDoctor(e.target.value)}
              className="form-select"
              id="doctor"
            >
              <option value="">Selecciona Doctor</option>
              {doctoresEncontrados.map((doc) => (
                <option key={doc.nombre} value={doc.nombre}>
                  {doc.nombre}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className="row mb-3">
          <div className="col-md-6">
            <label htmlFor="dia" className="form-label">
              Fecha
            </label>
            <DatePicker
              selected={dia}
              onChange={(date) => setDia(date)}
              dateFormat="dd/MM/yyyy"
              className="form-control"
              id="dia"
            />
          </div>
          <div className="col-md-6">
            <label htmlFor="hora" className="form-label">
              Hora
            </label>
            {/* <select
              value={hora}
              onChange={(e) => setHora(e.target.value)}
              className="form-select"
              id="hora"
            >
              <option value="">Selecciona Hora</option>
              {generarHoras().map((hora) => (
                <option key={hora} value={hora}>
                  {hora}
                </option>
              ))}
            </select> */}
          </div>
        </div>
        <div className="text-center">
          <button
            type="button"
            // onClick={solicitarCita}
            className="btn btn-primary"
          >
            Solicitar Cita
          </button>
        </div>
      </form>
    </div>
  );
}

export default Appointments;

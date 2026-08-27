import { useParams } from "react-router";

function CompanyDetail() {
  const { companyId } = useParams();
  return <div>CompanyDetail</div>;
}

export default CompanyDetail;
